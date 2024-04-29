from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import views, response
from rest_framework import status
from . import serializers
from . import email
from . import models
from . import tokens

User = get_user_model()


class Message:
    def warn(msg):
        return {"body": {"warn": msg}, "status": status.HTTP_406_NOT_ACCEPTABLE}

    def error(msg):
        return {"body": {"error": msg}, "status": status.HTTP_400_BAD_REQUEST}

    def success(msg):
        return {"body": {"success": msg}, "status": status.HTTP_200_OK}

    def create(msg):
        return {"body": {"success": msg}, "status": status.HTTP_201_CREATED}


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserViews(views.APIView):
    def create_uid(self):
        uid = tokens.create_uid()
        if models.ActivationCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self):
        token = tokens.create_token()
        if models.ActivationCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    def check_email_exists(self, email):
        return True if User.objects.filter(email=email).exists() else False

    def check_authenticated_user(self, user):
        return True if user.is_authenticated else False

    def get(self, request):
        try:
            if self.check_authenticated_user(request.user) is False:
                res = Message.error("You are not authenticated yet. Try again.")
                return response.Response(res["body"], status=res["status"])

            serialized_data = serializers.UserSerializer(request.user)
            res = Message.success(serialized_data.data)
            return response.Response(res["body"], status=res["status"])

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])

    def post(self, request):
        try:
            if self.check_email_exists(request.data["email"]):
                res = Message.warn("You have already registered.")
                return response.Response(res["body"], status=res["status"])

            serialized_data = serializers.UserCreateSerializer(data=request.data)

            if serialized_data.is_valid() is False:
                res = Message.error(
                    "There is some issue. User is not created. Try again."
                )
                return response.Response(res["body"], status=res["status"])

            user = serialized_data.save()
            models.ActivationCode.objects.create(
                user=user, uid=self.create_uid(), token=self.create_token()
            )
            email.ActivationEmail(user)
            res = Message.create("Your account has been creates. At First verify it.")
            return response.Response(
                {**res["body"], **{"user": user.email}}, status=res["status"]
            )

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])

    def patch(self, request):
        try:
            if self.check_authenticated_user(request.user) is False:
                res = Message.error("You are not authenticated yet. Try again.")
                return response.Response(res["body"], status=res["status"])

            user = User.objects.get(email=request.user.email)

            serialized_data = serializers.UserUpdateSerializer(
                user, data=request.data, partial=True
            )

            if serialized_data.is_valid() is False:
                res = Message.error("Your data is not valid. Try again.")
                return response.Response(res["body"], status=res["status"])

            serialized_data.save()
            res = Message.create("Your data is updated.")
            return response.Response(res["body"], status=res["status"])

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])

    def delete(self, request):
        try:
            if self.check_authenticated_user(request.user) is False:
                res = Message.error("You are not authenticated yet. Try again.")
                return response.Response(res["body"], status=res["status"])

            User.objects.get(email=request.user.email).delete()
            res = Message.success("Your account is deleted.")
            return response.Response(res["body"], status=res["status"])

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])


class ActivateUserViews(views.APIView):
    def get(self, request):
        try:
            uid = request.GET["uid"]
            token = request.GET["token"]
            user = (
                models.ActivationCode.objects.filter(uid=uid, token=token)[0].user
                if models.ActivationCode.objects.filter(uid=uid)
                .filter(token=token)
                .exists()
                else None
            )

            if user is None:
                res = Message.error("No such user is there. Try again.")
                return response.Response(res["body"], status=res["status"])

            parent_user = User.objects.get(email=user.email)
            parent_user.is_active = True
            parent_user.save()
            models.ActivationCode.objects.filter(uid=uid, token=token)[0].delete()

            res = Message.success("You are now verified.")
            return response.Response(
                {**res["body"], **get_tokens_for_user(parent_user)},
                status=res["status"],
            )

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])


class ResendActivateUserViews(views.APIView):
    def create_uid(self):
        uid = tokens.create_uid()
        if models.ActivationCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self):
        token = tokens.create_token()
        if models.ActivationCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    def check_email_exists(self, email):
        return True if User.objects.filter(email=email).exists() else False

    def get(self, request):
        try:
            user_email = request.GET["email"]

            if self.check_email_exists(user_email) is False:
                res = Message.error("No such user is there. Try again.")
                return response.Response(res["body"], status=res["status"])

            user = User.objects.get(email=user_email)

            if user.is_active is True:
                res = Message.error("You are already verified.")
                return response.Response(res["body"], status=res["status"])

            if models.ActivationCode.objects.filter(user=user).exists():
                models.ActivationCode.objects.get(user=user).delete()

            models.ActivationCode.objects.create(
                user=user, uid=self.create_uid(), token=self.create_token()
            )
            email.ActivationEmail(user)

            res = Message.success("Activation link has been sent to your email.")
            return response.Response(res["body"], status=res["status"])

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])


class CreateJWT(views.APIView):
    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]

            if User.objects.filter(email=email).exists() is False:
                res = Message.error("No such user is there. Try again.")
                return response.Response(res["body"], status=res["status"])

            user = authenticate(username=email, password=password)

            if user is None:
                res = Message.error("You are not authenticated properly. Try again.")
                return response.Response(res["body"], status=res["status"])

            if user.is_active is False:
                res = Message.error("You are not verified yet. Verify first.")
                return response.Response(res["body"], status=res["status"])

            res = Message.success("You are authenticated.")
            return response.Response(
                {**res["body"], **get_tokens_for_user(user)}, status=res["status"]
            )

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])


class ResetUserPassword(views.APIView):
    def check_authenticated_user(self, user):
        return True if user.is_authenticated else False

    def create_uid(self):
        uid = tokens.create_uid()
        if models.ActivationCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self):
        token = tokens.create_token()
        if models.ActivationCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    def get(self, request):
        try:
            if self.check_authenticated_user(request.user) is False:
                res = Message.error("You are not authenticated yet. Try again.")
                return response.Response(res["body"], status=res["status"])

            if models.ResetPasswordCode.objects.filter(user=request.user).exists():
                models.ResetPasswordCode.objects.get(user=request.user).delete()

            models.ResetPasswordCode.objects.create(
                user=request.user, uid=self.create_uid(), token=self.create_token()
            )
            email.ResetPasswordConfirmation(request.user)

            res = Message.success("Reset Password link is sent to your mail.")
            return response.Response(res["body"], status=res["status"])

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])

    def post(self, request):
        try:
            if self.check_authenticated_user(request.user) is False:
                res = Message.error("You are not authenticated yet. Try again.")
                return response.Response(res["body"], status=res["status"])

            new_password = request.data["new_password"]
            current_password = request.data["current_password"]
            uid = request.data["uid"]
            token = request.data["token"]

            if (
                models.ResetPasswordCode.objects.filter(uid=uid, token=token).exists()
                is False
            ):
                res = Message.error("There is some issue. Try again.")
                return response.Response(res["body"], status=res["status"])

            current_user = models.ResetPasswordCode.objects.filter(
                uid=uid, token=token
            )[0]

            if current_user.user.email != request.user.email:
                res = Message.error("There is some issue. Try again.")
                return response.Response(res["body"], status=res["status"])

            user = User.objects.get(email=request.user.email)

            if user.check_password(current_password) is False:
                res = Message.error("Your current password is not correct. Try again.")
                return response.Response(res["body"], status=res["status"])

            user.set_password(new_password)
            user.save()
            models.ResetPasswordCode.objects.get(user=request.user).delete()
            res = Message.success("Successfully changed the password")
            return response.Response(res["body"], status=res["status"])

        except Exception as e:
            res = Message.error(f"{e}")
            return response.Response(res["body"], status=res["status"])

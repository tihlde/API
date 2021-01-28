from django.utils.translation import gettext as _
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.common.permissions import IsDev, IsHS, get_user_id, is_admin_user
from app.group.models import Membership
from app.group.serializers import MembershipSerializer
from app.group.serializers.membership import (
    MembershipLeaderSerializer,
    UpdateMembershipSerializer,
)


class MembershipViewSet(viewsets.ModelViewSet):

    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()
    permission_classes = [IsDev | IsHS]
    lookup_field = "user_id"

    def get_queryset(self):
        return self.queryset.filter(group__slug=self.kwargs["slug"])

    def get_permissions(self):
        if is_admin_user(self.request):
            self.serializer_class = MembershipLeaderSerializer
        if Membership.is_leader(get_user_id(self.request), self.kwargs["slug"]):
            self.permission_classes = []
            self.serializer_class = MembershipLeaderSerializer
        if self.request.method == "GET":
            self.permission_classes = []
        return super(MembershipViewSet, self).get_permissions()

    def update(self, request, *args, **kwargs):
        try:
            membership = self.get_object()
            serializer = UpdateMembershipSerializer(
                membership, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            return super().update(request, *args, **kwargs)
        except Membership.DoesNotExist:
            return Response(
                {"detail": _("Medlemskapet eksisterer ikke")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def create(self, request, *args, **kwargs):
        try:
            membership = Membership.objects.get_or_create(
                user__user_id=request.data["user"]["user_id"],
                group__slug=kwargs["slug"],
            )

            serializer = MembershipSerializer(membership[0], data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Membership.DoesNotExist:
            return Response(
                {"detail": _("Medlemskapet eksisterer ikke")},
                status=status.HTTP_404_NOT_FOUND,
            )

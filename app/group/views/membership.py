from django.utils.translation import gettext as _
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.common.permissions import IsDev, IsHS, IsNoKorPromo
from app.content.models import User
from app.group.models import Group, Membership
from app.group.serializers import MembershipSerializer
from app.group.serializers.membership import UpdateMembershipSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    """API endpoint for Groups"""

    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()
    permission_classes = [IsNoKorPromo]
    lookup_field = "user_id"

    def get_queryset(self):
        return self.queryset.filter(group__slug=self.kwargs["slug"])

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = []
        if self.action == "destroy":
            self.permisson_classes = [IsHS | IsDev]
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
            group = Group.objects.get(slug=kwargs["slug"])
            user = User.objects.get(user_id=request.data["user"]["user_id"])
            membership = Membership.objects.get_or_create(user=user, group=group)
            serializer = MembershipSerializer(membership[0], data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except Membership.DoesNotExist:
            return Response(
                {"detail": _("Medlemskapet eksisterer ikke")},
                status=status.HTTP_404_NOT_FOUND,
            )

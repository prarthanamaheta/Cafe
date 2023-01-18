from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class ModeratorRequiredMixin(LoginRequiredMixin):
    """
    User requires moderator permission
    """

    def dispatch(self, request, *args, **kwargs):
        """
        role required dispatch method
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied

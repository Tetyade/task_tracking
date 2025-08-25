from django.core.exceptions import PermissionDenied

class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
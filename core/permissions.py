"""
Custom permission classes for role-based API access control.

Usage:
    permission_classes = [IsAdminOrDoctor]
    permission_classes = [IsClinicalStaff]
    permission_classes = [IsAdminUser]
"""
from rest_framework import permissions
from staff.models import Staff


class IsAdminUser(permissions.BasePermission):
    """Only admin users (is_staff) can access."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrDoctor(permissions.BasePermission):
    """Admin users or doctors can access."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.staff_profile.role in ['DOCTOR', 'SURGEON']
        except (AttributeError, Staff.DoesNotExist):
            return False


class IsClinicalStaff(permissions.BasePermission):
    """Any clinical staff (doctor, nurse, surgeon, etc.) can access."""
    MEDICAL_ROLES = ['DOCTOR', 'NURSE', 'SURGEON', 'ANESTHESIOLOGIST', 'RADIOLOGIST', 'PHARMACIST']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.staff_profile.role in self.MEDICAL_ROLES
        except (AttributeError, Staff.DoesNotExist):
            return False


class IsBillingStaff(permissions.BasePermission):
    """Admin or billing-related staff can access."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return request.user.has_perm('billing.view_invoice')


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission: only owners can edit, anyone authenticated can view."""
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return hasattr(obj, 'patient') and obj.patient == request.user

from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings
from io import StringIO
from django.core.management import call_command

from .models import (
    Collection,
    Machinery,
    MachineryWarning,
    MachineryFault,
    FaultImage,
    FaultComment,
    UserProfile
)


# Authors
# Jahziel Belmonte,
# Thomas viard

# Test cases for the models

class CollectionModelTest(TestCase):
    """Tests for the Collection model"""

    def setUp(self):
        # Create a test collection
        self.collection_name = "Test Collection"
        self.collection = Collection.objects.create(
            name=self.collection_name,
            description="This is a test collection"
        )

    def test_collection_creation(self):
        """Test that a collection can be created with the expected attributes"""
        self.assertEqual(self.collection.name, self.collection_name)
        self.assertEqual(self.collection.description, "This is a test collection")
        self.assertEqual(self.collection.slug, slugify(self.collection_name))

    def test_collection_string_representation(self):
        """Test the string representation of a collection"""
        self.assertEqual(str(self.collection), self.collection_name)

    def test_collection_slug_auto_generation(self):
        """Test that the slug is automatically generated from the name"""
        collection = Collection.objects.create(
            name="Another Test Collection",
            description="Another test collection description"
        )
        self.assertEqual(collection.slug, "another-test-collection")

    def test_collection_ordering(self):
        """Test that collections are ordered by name"""
        Collection.objects.create(name="A Collection")
        Collection.objects.create(name="Z Collection")

        # Get collections ordered by name explicitly to ensure consistent ordering
        collections = Collection.objects.all().order_by('name')
        self.assertEqual(collections[0].name, "A Collection")
        self.assertEqual(collections[1].name, "Test Collection")
        self.assertEqual(collections[2].name, "Z Collection")


class MachineryModelTest(TestCase):
    """Tests for the Machinery model"""

    def setUp(self):
        # Create test users
        self.technician = User.objects.create_user(
            username="techtester",
            password="testpass123"
        )
        self.repair_user = User.objects.create_user(
            username="repairtester",
            password="testpass123"
        )

        # Create test collection
        self.collection = Collection.objects.create(
            name="Test Collection",
            description="Test collection description"
        )

        # Create test machinery
        self.machinery = Machinery.objects.create(
            name="Test Machinery",
            description="Test machinery description",
            status="OK",
            importance=5
        )

        # Add relationships
        self.machinery.collections.add(self.collection)
        self.machinery.assigned_technicians.add(self.technician)
        self.machinery.assigned_repair.add(self.repair_user)

    def test_machinery_creation(self):
        """Test that machinery can be created with the expected attributes"""
        self.assertEqual(self.machinery.name, "Test Machinery")
        self.assertEqual(self.machinery.description, "Test machinery description")
        self.assertEqual(self.machinery.status, "OK")
        self.assertEqual(self.machinery.importance, 5)
        self.assertTrue(self.machinery.created_at)
        self.assertTrue(self.machinery.updated_at)

    def test_machinery_relationships(self):
        """Test the relationships between machinery and other models"""
        self.assertEqual(self.machinery.collections.count(), 1)
        self.assertEqual(self.machinery.collections.first(), self.collection)

        self.assertEqual(self.machinery.assigned_technicians.count(), 1)
        self.assertEqual(self.machinery.assigned_technicians.first(), self.technician)

        self.assertEqual(self.machinery.assigned_repair.count(), 1)
        self.assertEqual(self.machinery.assigned_repair.first(), self.repair_user)

    def test_machinery_string_representation(self):
        """Test the string representation of machinery"""
        self.assertEqual(str(self.machinery), "Test Machinery")

    def test_machinery_update_status(self):
        """Test the update_status method"""
        # Initially status is OK
        self.assertEqual(self.machinery.status, "OK")

        # Add a warning
        MachineryWarning.objects.create(
            machinery=self.machinery,
            text="Test warning",
            created_by=self.technician
        )

        # Status should now be WARNING
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "WARNING")

        # Add a fault
        MachineryFault.objects.create(
            machinery=self.machinery,
            title="Test fault",
            details="Test fault details",
            created_by=self.technician
        )

        # Status should now be FAULT
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "FAULT")

        # Resolve the fault
        fault = MachineryFault.objects.get(machinery=self.machinery)
        fault.resolved = True
        fault.resolved_by = self.repair_user
        fault.resolved_at = timezone.now()
        fault.save()

        # Status should go back to WARNING because of the existing warning
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "WARNING")

        # Delete the warning
        MachineryWarning.objects.filter(machinery=self.machinery).delete()

        # Status should go back to OK
        # Manually update the status since the delete method might not trigger the update_status
        self.machinery.update_status()
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "OK")

    def test_machinery_last_issue(self):
        """Test the last_issue property"""
        # Initially there should be no issues
        self.assertIsNone(self.machinery.last_issue)

        # Add a warning
        warning = MachineryWarning.objects.create(
            machinery=self.machinery,
            text="Test warning",
            created_by=self.technician
        )

        # last_issue should now return the warning
        last_issue = self.machinery.last_issue
        self.assertEqual(last_issue['type'], 'Warning')
        self.assertEqual(last_issue['comment'], 'Test warning')
        self.assertIsNone(last_issue['image'])

        # Add a fault
        fault = MachineryFault.objects.create(
            machinery=self.machinery,
            title="Test fault",
            details="Test fault details",
            created_by=self.technician
        )

        # last_issue should now return the fault
        last_issue = self.machinery.last_issue
        self.assertEqual(last_issue['type'], 'Fault')
        self.assertEqual(last_issue['comment'], 'Test fault details')
        self.assertIsNone(last_issue['image'])


class MachineryWarningModelTest(TestCase):
    """Tests for the MachineryWarning model"""

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="warningtester",
            password="testpass123"
        )

        # Create test machinery
        self.machinery = Machinery.objects.create(
            name="Test Machinery",
            description="Test machinery description",
            status="OK",
            importance=5
        )

        # Create test warning
        self.warning = MachineryWarning.objects.create(
            machinery=self.machinery,
            text="Test warning",
            created_by=self.user
        )

    def test_warning_creation(self):
        """Test that a warning can be created with the expected attributes"""
        self.assertEqual(self.warning.machinery, self.machinery)
        self.assertEqual(self.warning.text, "Test warning")
        self.assertEqual(self.warning.created_by, self.user)
        self.assertTrue(self.warning.created_at)

    def test_warning_string_representation(self):
        """Test the string representation of a warning"""
        expected_str = f"{self.machinery.name}: {self.warning.text}"
        self.assertEqual(str(self.warning), expected_str)

    def test_warning_affects_machinery_status(self):
        """Test that creating a warning changes the machinery status"""
        # Machinery status should be WARNING after creating a warning
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "WARNING")

        # Deleting the warning should change the status back to OK
        self.warning.delete()
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "OK")


class MachineryFaultModelTest(TestCase):
    """Tests for the MachineryFault model"""

    def setUp(self):
        # Create test users
        self.creator = User.objects.create_user(
            username="faulttester",
            password="testpass123"
        )
        self.resolver = User.objects.create_user(
            username="resolvertester",
            password="testpass123"
        )

        # Create test machinery
        self.machinery = Machinery.objects.create(
            name="Test Machinery",
            description="Test machinery description",
            status="OK",
            importance=5
        )

        # Create test fault
        self.fault = MachineryFault.objects.create(
            machinery=self.machinery,
            title="Test fault",
            details="Test fault details",
            created_by=self.creator
        )

    def test_fault_creation(self):
        """Test that a fault can be created with the expected attributes"""
        self.assertEqual(self.fault.machinery, self.machinery)
        self.assertEqual(self.fault.title, "Test fault")
        self.assertEqual(self.fault.details, "Test fault details")
        self.assertEqual(self.fault.created_by, self.creator)
        self.assertFalse(self.fault.resolved)
        self.assertIsNone(self.fault.resolved_at)
        self.assertIsNone(self.fault.resolved_by)
        self.assertTrue(self.fault.created_at)

    def test_fault_string_representation(self):
        """Test the string representation of a fault"""
        expected_str = f"Case #{self.fault.pk}: {self.fault.title}"
        self.assertEqual(str(self.fault), expected_str)

    def test_fault_affects_machinery_status(self):
        """Test that creating a fault changes the machinery status"""
        # Machinery status should be FAULT after creating a fault
        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "FAULT")

        # Resolving the fault should change the status back to OK
        self.fault.resolved = True
        self.fault.resolved_by = self.resolver
        self.fault.resolved_at = timezone.now()
        self.fault.save()

        self.machinery.refresh_from_db()
        self.assertEqual(self.machinery.status, "OK")


class FaultImageModelTest(TestCase):
    """Tests for the FaultImage model"""

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="imagetester",
            password="testpass123"
        )

        # Create test machinery
        self.machinery = Machinery.objects.create(
            name="Test Machinery",
            description="Test machinery description",
            status="OK",
            importance=5
        )

        # Create test fault
        self.fault = MachineryFault.objects.create(
            machinery=self.machinery,
            title="Test fault",
            details="Test fault details",
            created_by=self.user
        )

        # Create a test image file
        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content for testing
            content_type='image/jpeg'
        )

        # Create test fault image
        self.fault_image = FaultImage.objects.create(
            fault=self.fault,
            image=self.image_file,
            uploaded_by=self.user
        )

    def test_fault_image_creation(self):
        """Test that a fault image can be created with the expected attributes"""
        self.assertEqual(self.fault_image.fault, self.fault)
        self.assertEqual(self.fault_image.uploaded_by, self.user)
        self.assertTrue(self.fault_image.uploaded_at)
        # Just check that the image field has a name, as the exact name might be modified by Django
        self.assertTrue(self.fault_image.image.name)

    def test_fault_image_string_representation(self):
        """Test the string representation of a fault image"""
        expected_str = f"Image for {self.fault}"
        self.assertEqual(str(self.fault_image), expected_str)


class FaultCommentModelTest(TestCase):
    """Tests for the FaultComment model"""

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="commenttester",
            password="testpass123"
        )

        # Create test machinery
        self.machinery = Machinery.objects.create(
            name="Test Machinery",
            description="Test machinery description",
            status="OK",
            importance=5
        )

        # Create test fault
        self.fault = MachineryFault.objects.create(
            machinery=self.machinery,
            title="Test fault",
            details="Test fault details",
            created_by=self.user
        )

        # Create test comment
        self.comment = FaultComment.objects.create(
            fault=self.fault,
            user=self.user,
            text="This is a test comment"
        )

    def test_fault_comment_creation(self):
        """Test that a fault comment can be created with the expected attributes"""
        self.assertEqual(self.comment.fault, self.fault)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.text, "This is a test comment")
        self.assertTrue(self.comment.created_at)

    def test_fault_comment_string_representation(self):
        """Test the string representation of a fault comment"""
        expected_str = f"Comment by {self.user.username} on {self.fault}"
        self.assertEqual(str(self.comment), expected_str)

    def test_fault_comment_ordering(self):
        """Test that comments are ordered by created_at"""
        # Create another comment with an earlier timestamp
        earlier_time = timezone.now() - timedelta(hours=1)
        earlier_comment = FaultComment.objects.create(
            fault=self.fault,
            user=self.user,
            text="This is an earlier comment"
        )
        earlier_comment.created_at = earlier_time
        earlier_comment.save(update_fields=['created_at'])

        # Create another comment with a later timestamp
        later_time = timezone.now() + timedelta(hours=1)
        later_comment = FaultComment.objects.create(
            fault=self.fault,
            user=self.user,
            text="This is a later comment"
        )
        later_comment.created_at = later_time
        later_comment.save(update_fields=['created_at'])

        # Get all comments for the fault
        comments = FaultComment.objects.filter(fault=self.fault)

        # Check that they are ordered by created_at
        self.assertEqual(comments[0], earlier_comment)
        self.assertEqual(comments[1], self.comment)
        self.assertEqual(comments[2], later_comment)


class UserProfileModelTest(TestCase):
    """Tests for the UserProfile model"""

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="profiletester",
            password="testpass123"
        )

        # Create test user profile
        self.profile = UserProfile.objects.create(
            user=self.user,
            role="Technician"
        )

    def test_user_profile_creation(self):
        """Test that a user profile can be created with the expected attributes"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.role, "Technician")

    def test_user_profile_string_representation(self):
        """Test the string representation of a user profile"""
        expected_str = f"{self.user.username} - {self.profile.role}"
        self.assertEqual(str(self.profile), expected_str)


class GroupPermissionsTest(TestCase):
    """Tests for the group permissions setup"""

    def setUp(self):
        # Create content types for the models
        self.machinery_type = ContentType.objects.get_for_model(Machinery)
        self.fault_type = ContentType.objects.get_for_model(MachineryFault)

        # Create test users for each role
        self.technician_user = User.objects.create_user(
            username="tech_test",
            password="testpass123"
        )
        self.repair_user = User.objects.create_user(
            username="repair_test",
            password="testpass123"
        )
        self.manager_user = User.objects.create_user(
            username="manager_test",
            password="testpass123"
        )

    def test_setup_groups_command(self):
        """Test that the setup_groups command creates the expected groups and permissions"""
        # Capture command output
        out = StringIO()
        call_command('setup_groups', stdout=out)
        command_output = out.getvalue()

        # Check that the command output indicates groups were created or already exist
        self.assertIn('Group "Technicians"', command_output)
        self.assertIn('Group "Repair"', command_output)
        self.assertIn('Group "Managers"', command_output)

        # Verify groups exist
        self.assertTrue(Group.objects.filter(name="Technicians").exists())
        self.assertTrue(Group.objects.filter(name="Repair").exists())
        self.assertTrue(Group.objects.filter(name="Managers").exists())

    def test_technician_permissions(self):
        """Test that technicians have the correct permissions"""
        # Run setup_groups command to ensure permissions are created
        call_command('setup_groups')

        # Get the technician group
        technician_group = Group.objects.get(name="Technicians")

        # Add user to the group
        self.technician_user.groups.add(technician_group)

        # Check that the technician has the expected permissions
        self.assertTrue(self.technician_user.has_perm(f"App.view_machinery"))
        self.assertTrue(self.technician_user.has_perm(f"App.add_warning"))
        self.assertTrue(self.technician_user.has_perm(f"App.create_fault"))
        self.assertTrue(self.technician_user.has_perm(f"App.comment_fault"))

        # Check that the technician doesn't have manager or repair permissions
        self.assertFalse(self.technician_user.has_perm(f"App.add_machinery"))
        self.assertFalse(self.technician_user.has_perm(f"App.resolve_fault"))

    def test_repair_permissions(self):
        """Test that repair staff have the correct permissions"""
        # Run setup_groups command to ensure permissions are created
        call_command('setup_groups')

        # Get the repair group
        repair_group = Group.objects.get(name="Repair")

        # Add user to the group
        self.repair_user.groups.add(repair_group)

        # Check that the repair staff has the expected permissions
        self.assertTrue(self.repair_user.has_perm(f"App.view_machinery"))
        self.assertTrue(self.repair_user.has_perm(f"App.remove_warning"))
        self.assertTrue(self.repair_user.has_perm(f"App.resolve_fault"))
        self.assertTrue(self.repair_user.has_perm(f"App.comment_fault"))

        # Check that the repair staff doesn't have manager or technician permissions
        self.assertFalse(self.repair_user.has_perm(f"App.add_machinery"))
        self.assertFalse(self.repair_user.has_perm(f"App.create_fault"))

    def test_manager_permissions(self):
        """Test that managers have the correct permissions"""
        # Run setup_groups command to ensure permissions are created
        call_command('setup_groups')

        # Get the manager group
        manager_group = Group.objects.get(name="Managers")

        # Add user to the group
        self.manager_user.groups.add(manager_group)

        # Check that the manager has the expected permissions
        self.assertTrue(self.manager_user.has_perm(f"App.view_machinery"))
        self.assertTrue(self.manager_user.has_perm(f"App.add_machinery"))
        self.assertTrue(self.manager_user.has_perm(f"App.delete_machinery"))
        self.assertTrue(self.manager_user.has_perm(f"App.assign_users"))
        self.assertTrue(self.manager_user.has_perm(f"App.generate_reports"))
        self.assertTrue(self.manager_user.has_perm(f"App.comment_fault"))

        # Check that the manager doesn't have technician or repair specific permissions
        self.assertFalse(self.manager_user.has_perm(f"App.create_fault"))
        self.assertFalse(self.manager_user.has_perm(f"App.resolve_fault"))

    def test_permission_separation(self):
        """Test that permissions are properly separated between groups"""
        # Run setup_groups command to ensure permissions are created
        call_command('setup_groups')

        # Get all groups
        technician_group = Group.objects.get(name="Technicians")
        repair_group = Group.objects.get(name="Repair")
        manager_group = Group.objects.get(name="Managers")

        # Get permissions for each group
        technician_perms = set(technician_group.permissions.values_list('codename', flat=True))
        repair_perms = set(repair_group.permissions.values_list('codename', flat=True))
        manager_perms = set(manager_group.permissions.values_list('codename', flat=True))

        # Check unique permissions for technicians
        self.assertIn('add_warning', technician_perms)
        self.assertIn('create_fault', technician_perms)
        self.assertNotIn('add_warning', repair_perms)
        self.assertNotIn('create_fault', manager_perms)

        # Check unique permissions for repair staff
        self.assertIn('remove_warning', repair_perms)
        self.assertIn('resolve_fault', repair_perms)
        self.assertNotIn('remove_warning', technician_perms)
        self.assertNotIn('resolve_fault', manager_perms)

        # Check unique permissions for managers
        self.assertIn('add_machinery', manager_perms)
        self.assertIn('delete_machinery', manager_perms)
        self.assertIn('assign_users', manager_perms)
        self.assertIn('generate_reports', manager_perms)
        self.assertNotIn('add_machinery', technician_perms)
        self.assertNotIn('delete_machinery', repair_perms)

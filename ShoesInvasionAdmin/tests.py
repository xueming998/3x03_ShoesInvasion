from django.test import TestCase, Client
from ShoesInvasionApp.models.user import UserTable

# HTTP Response Code Legend
# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_302_FOUND
# HTTP_404_NOT_FOUND

# Test if pages loads properly
class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('/ShoesInvasionAdmin/')
        self.assertEqual(response.status_code, 200)

# Admin Test Case
class AdminTestCase(TestCase):
    def setUp(self):
        adminUser = UserTable.objects.create(
            first_name = "Elon",
            last_name = "Musk",
            username = "elonmusk",
            password = "teslatwitterez",
            verify_password = "teslatwitterez",
            email = "elonmusk@twitter.com",
            phone = 87657987,
            bannedStatus = 0,
            verifiedStatus = 1,
            verificationCode = "2i4othlsad",
            lockedStatus = 0,
            lockedCounter = 0,
            accountType = "Admin",
            unique_id = "1l3rjjr1212bju13rbjuo1br5j3q",
            secret_key = ""
        )
        adminUser2 = UserTable.objects.create(
            first_name = "Jack",
            last_name = "Ma",
            username = "jackma",
            password = "alibababillionair",
            verify_password = "alibababillionair",
            email = "jackma@alibaba.com",
            phone = 87657984,
            bannedStatus = 0,
            verifiedStatus = 1,
            verificationCode = "2i4otasglsad",
            lockedStatus = 0,
            lockedCounter = 0,
            accountType = "Admin",
            unique_id = "iokwrsngio32klt4nho1iqnf",
            secret_key = "NICN1K32512L3KN5"
        )
        user = UserTable.objects.create(
            first_name = "Warren",
            last_name = "Buffett",
            username = "warrenbuffett",
            password = "investingiseasy",
            verify_password = "investingiseasy",
            email = "buffett@berkshire.com",
            phone = 87657184,
            bannedStatus = 0,
            verifiedStatus = 1,
            verificationCode = "2ikq24nepi4otasglsad",
            lockedStatus = 0,
            lockedCounter = 0,
            accountType = "User",
            unique_id = "io1obr3jlkkwrsngio32klt4nho1iqnf",
            secret_key = "NICN1K322KLTN1Q3512L3KN5"
        )
        adminUser.save()
        adminUser2.save()
        user.save()

    def test_admin_can_get_details(self):
        adminUsername = UserTable.objects.get(username = "elonmusk")
        self.assertEqual(adminUsername.email, "elonmusk@twitter.com")
        self.assertEqual(adminUsername.unique_id, "1l3rjjr1212bju13rbjuo1br5j3q")
        
        adminUsername2 = UserTable.objects.get(username = "jackma")
        self.assertEqual(adminUsername2.email, "jackma@alibaba.com")
        self.assertEqual(adminUsername2.unique_id, "iokwrsngio32klt4nho1iqnf")

    def test_admin_login_without_otp(self):
        c = Client()
        response = c.post('/ShoesInvasionAdmin/login', {'username': 'elonmusk', 'password': 'teslatwitterez', "otpToken": ""})
        self.assertEqual(response.status_code, 200)

    def test_admin_login_with_otp(self):
        c2 = Client()
        response2 = c2.post('/ShoesInvasionAdmin/login', {'username': 'jackma', 'password': 'alibababillionair', "otpToken": "4546321"})
        self.assertEqual(response2.status_code, 200)

    def test_admin_ban_user(self):
        c3 = Client()
        userBanned = UserTable.objects.get(username = "warrenbuffett")
        # bannedStatus = 0 means account not banned
        self.assertFalse(userBanned.bannedStatus)
        response3 = c3.post('/ShoesInvasionAdmin/ban_unban/', {'uid': 'io1obr3jlkkwrsngio32klt4nho1iqnf'})
        self.assertEqual(response3.status_code, 200)
        # bannedStatus = 1 means account banned
        self.assertTrue(response3.content)

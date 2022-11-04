from django.test import TestCase, Client
from ShoesInvasionApp.models.user import UserTable

# Create your tests here.

# HTTP Response Code Legend
# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_302_FOUND
# HTTP_404_NOT_FOUND

# Test if pages loads properly
class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('/ShoesInvasionEditor/')
        self.assertEqual(response.status_code, 200)

# Test to create product and extract details from table
class EditorTestCase(TestCase):
    # Setting up the test case by creating a new product
    def setUp(self):
        editorUser = UserTable.objects.create(
            first_name = "Jeff",
            last_name = "Bezos",
            username = "jeffbezos",
            password = "amazonecommerce",
            verify_password = "amazonecommerce",
            email = "jeffbezos@amazon.com",
            phone = 87657187,
            bannedStatus = 0,
            verifiedStatus = 1,
            verificationCode = "2i4tpkl2",
            lockedStatus = 0,
            lockedCounter = 0,
            accountType = "Editor",
            unique_id = "3nklqyg3klern5y",
            secret_key = "LC1J2K35LC1JK235")

        editorUser2 = UserTable.objects.create(
            first_name = "Bill",
            last_name = "Gates",
            username = "billgates",
            password = "windows11ezmoney",
            verify_password = "windows11ezmoney",
            email = "billgates@microsoft.com",
            phone = 89657187,
            bannedStatus = 0,
            verifiedStatus = 1,
            verificationCode = "b1olrjn1o",
            lockedStatus = 0,
            lockedCounter = 0,
            accountType = "Editor",
            unique_id = "t43ionop3nr1p1onm31ft1")
        editorUser.save()
        editorUser2.save()

    def test_admin_can_get_details(self):
        # New Product added as shown above
        editorUsername = UserTable.objects.get(username = "jeffbezos")
        self.assertEqual(editorUsername.email, "jeffbezos@amazon.com")
        self.assertEqual(editorUsername.unique_id, "3nklqyg3klern5y")
        
        adminUsername2 = UserTable.objects.get(username = "billgates")
        self.assertEqual(adminUsername2.email, "billgates@microsoft.com")
        self.assertEqual(adminUsername2.unique_id, "t43ionop3nr1p1onm31ft1")

    def test_login_loads_properly(self):
        response = self.client.get('/ShoesInvasionEditor/login')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='ShoesInvasionEditor/login.html')

    def test_login(self):
        c = Client()
        # Dummy OTP because OTP is required to login but for unit test, unable to generate QR Code to do
        response = c.post('/ShoesInvasionEditor/login', {'username': 'jeffbezos', 'password': 'amazonecommerce', "otpToken": "123456"})
        self.assertEqual(response.status_code, 200)
        c = Client()
        response2 = c.post('/ShoesInvasionEditor/login', {'username': 'billgates', 'password': 'windows11ezmoney', "otpToken": ""})
        self.assertEqual(response2.status_code, 200)

    def test_create_product(self):
        session = self.client.session
        session['unique_id'] ='3nklqyg3klern5y'
        session.save()
        response = self.client.post('/ShoesInvasionEditor/create', 
        {'product_name': 'Air Jordan 2 Retro SE',
         'product_price': '355', 
         "product_info": "Air Jordan 2 made its debut in 1987 as a sleeker, more streamlined version of its predecessor. This version of the AJ 2 features premium leather and an Air-Sole unit, making it the ultimate combination of performance and style.",
         "product_brand": "Nike",
         "status": "2",
         "gender": "F",
         "category": "Sneakers"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'manage')
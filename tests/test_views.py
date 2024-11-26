from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse


from authentication.models import User
from api.models import Ad, Comment


class LoginViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='username1', email="user1@gmail.com", password="User1@1234", name="user1")
    
    def test_authentication(self):
        response = self.client.post(reverse('login'), {'email': 'user1@gmail.com', 'password': 'User1@1234'})
        self.assertEqual(response.status_code, 200)
        user = authenticate(email='user1@gmail.com', password='User1@1234')
        self.assertIsNotNone(user)


class AdCommentViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', email="user1@gmail.com", password="User1@1234", name="user1")
        self.user2 = User.objects.create_user(username='username2', email="user2@gmail.com", password="User2@1234", name="user2")

        self.ad1 = Ad.objects.create(author=self.user1, title='title1', content='content1')
        self.ad2 = Ad.objects.create(author=self.user2, title='title2', content='content2')

        self.comment1 = Comment.objects.create(author=self.user1, ad=self.ad1, content='comment1')
        self.comment2 = Comment.objects.create(author=self.user1, ad=self.ad2, content='comment2')

    def test_ad_create(self):
        self.client.login(email='user1@gmail.com', password='User1@1234')
        response = self.client.post(reverse('ad-create'), {'title': 'title1', 'content': 'content1'})
        response_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['title'], 'title1')
        self.assertEqual(response_data['content'], 'content1')
    
    def test_ad_list(self):
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data[0]['author'], 'user1')
        self.assertEqual(response_data[0]['title'], 'title1')
        self.assertEqual(response_data[0]['content'], 'content1')
        self.assertEqual(response_data[1]['author'], 'user2')
        self.assertEqual(response_data[1]['title'], 'title2')
        self.assertEqual(response_data[1]['content'], 'content2')
    
    def test_ad_update_success(self):
        self.client.login(email='user1@gmail.com', password='User1@1234')
        response = self.client.patch(f'/api/ads/update/{self.ad1.id}/', {'title': 'new title1'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['title'], 'new title1')
        self.assertEqual(response_data['content'], 'content1')

    # def test_ad_update_fail(self):
    #     self.client.login(email='user1@gmail.com', password='User1@1234')
    #     response = self.client.patch(f'/api/ads/update/{self.ad2.id}/', {'title': 'new title1'}, content_type='application/json')
    #     self.assertEqual(response.status_code, 401)

    def test_ad_detail(self):
        self.client.login(email='user2@gmail.com', password='User2@1234')
        response = self.client.get(f'/api/ads/detail/{self.ad2.id}/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['title'], 'title2')
        self.assertEqual(response_data['content'], 'content2')

    def test_ad_delete(self):
        self.client.login(email='user2@gmail.com', password='User2@1234')
        response = self.client.delete(f'/api/ads/detail/{self.ad2.id}/')
        self.assertEqual(response.status_code, 204)

    def test_ad_list_with_comment(self):
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data[0]['comments'][0]['author'], 'user1')
        self.assertEqual(response_data[0]['comments'][0]['ad'], self.ad1.id)
        self.assertEqual(response_data[0]['comments'][0]['content'], 'comment1')
    
    def test_create_commment_success(self):
        User.objects.create_user(username='username3', email="user3@gmail.com", password="User3@1234", name="user3")
        self.client.login(email='user3@gmail.com', password='User3@1234')
        response = self.client.post(reverse('comment-create'), {'ad': self.ad1.id, 'content': 'new comment'})
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['ad'], self.ad1.id)
        self.assertEqual(response_data['content'], 'new comment')

    def test_create_commment_fail(self):
        self.client.login(email='user1@gmail.com', password='User1@1234')
        response = self.client.post(reverse('comment-create'), {'ad': self.ad1.id, 'content': 'new comment'})
        self.assertEqual(response.status_code, 405)
        response_data = response.json()
        self.assertEqual(response_data['detail'], 'you cannot post comments more than once')


    

        
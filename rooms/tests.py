from rest_framework.test import APITestCase
from . import models
from users.models import User

# Create your tests here.


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenities/"

    # 다른 모든 테스트들이 실행되기 전에 수행된는 메소드이다. => 테스트 데이터베이스를 설정할 수 있는 곳이다.
    def setUp(self) -> None:
        # DB에 새로운 Amenity객체를 하나 생성한다.
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    # GET Method Test
    def test_all_amenities(self):
        # self.client는 우리가 API로 get/post/delete/put request를 보낼 수 있게 해준다.
        response = self.client.get(
            self.URL
        )  # 테스트 DB에서 room들의 amenities를 제대로 가지고 오는지를 검사
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    # POST Method Test
    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )
        data = response.json()  # POST하면 생성된 객체를 Response함수로 리턴헸었다.

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenity_description,
        )

        # ERROR CHECK
        response = self.client.post(self.URL)  # Without DATA
        data = response.json()
        self.assertEqual(response.status_code, 400)  # Bad Request Status Code 400
        self.assertIn("name", data)  # "name" should be in the error emssage

    ## 2024.04.08 Introduction

    # Method 이름 앞에 'test_' 키워드를 붙여야 자동으로 실행된다.
    # def test_twoPlustwo(self):
    #     self.assertEqual(2 + 2, 5, msg="Wrong Circulation")


class TestAmenity(APITestCase):

    NAME = "Test Amenity"
    DESC = "Test Dsc"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")

        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."
        # your code challenge
        # put을 바꾸는 조건이 많으니까 안 바꿀때를 검사하면 된다.
        response = self.client.put(
            "/api/v1/rooms/amenities/1",
        )
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 Status Code",
        )
        data = response.json()
        self.assertLessEqual(
            len(data["name"]),
            150,
            "Name is too long, max is 150 chracters",
        )
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_delete_amenity(self):

        response = self.client.delete("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")  # not requirement
        user.save()
        self.user = user  # class 내부의 user에 user를 저장한다.

    # to test Authentication
    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(
            response.status_code,
            403,
            "You are forbidden!",
        )
        self.client.force_login(  # username, password 필요없다. 유저 객체만 있으면 가능
            self.user,
        )
        # self.client.login(
        #     username:"test",
        #     password:"123",
        # )

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(
            response.status_code,
            400,
            "You are forbidden!",
        )

# Foodfeed Backend Server
## Technologies
Storage: PostgreSQL (Database) + S3 Bucket (File blobs) + Redis (In-memory caching)

Data Retrieval: BeautifulSoup + Selenium, crawled **29,558** shops and **712,733** food items around **Ho Chi Minh City**

API Deployment: Django

Server Deployment: Docker, AWS EC2 - Ubuntu Instance

## Instruction

0. Put the private files into folder foodfeed_app (.env and .json files)

1. Update the conda

```
conda update --all
```

3. Create a new virtual environment with Python and activate it.

```
cd Backend/
python -m venv env
source env/bin/activate
```

**Suggestion**: Using `conda`  if you don't want to use Python venv.
```
conda create -n backend
conda activate backend
```

2. Install the dependencies (The hardest one)

```
conda install -r requirements.txt
```

- if the installation fails, run the below code to check missing modules.

  ```
    python manage.py runserver
  ```

  Some modules may occur for installation.

  ```
    pip install python-dotenv supabase psycopg2-binary django-cors-headers geopy redis
  ```

3. Run the application (make sure you have PostgreSQL running on your machine and please change the database settings in settings.py to your own database settings...)

```
  python manage.py makemigrations
  python manage.py migrate 
  python manage.py runserver
```

4. Build the Docker image and run the container using the following commands:

```
  docker build -t foodfeed_django_backend .
  docker run -d -p 8000:8000 foodfeed_django_backend
```

  TODO: Use Docker-compose to automate deployment

5. *(Optional - Should use when running on a server)* Deploy Backend on **ngrok**

- Open a new terminal and run **ngrok**:
  ```
    ngrok http 8000
  ```

- If not using **ngrok**, just use the localhost [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Documentation

![Database Design](dbdesign.png)
### /users
#### `/login`
Login to existing user in the database.
##### POST
```js
{
  email: "yangtuananh2003@gmail.com",
  password: "123456"
}
```
returns
```js
{
  status: "You are now logged in
}
```

#### `/register`
Create new user in case they haven't existed in the database.
##### POST
```js
{
  full_name: "Yang Tuan Anh", 
  username: "yangtuananh", 
  email: "yangtuananh2003@gmail.com", 
  phone_number: "91311699", 
  password: "123456", 
  password2: "123456"
}
```
if valid input and user hasnt existed, returns
```js
{
  status: "You are now logged in
}
```
as automatic login after successful registration

#### `/logout`
Logout of current session.
##### POST
```js
{
  status: "You are now logged out"
}
```
#### `/profile`
Login required, returns the profile of the currently logged in user.
##### PUT
```js
{
  full_name: "Yang Tuấn Anh",
  bio: "why would you buy a dragonfruit from Singapore just to show it off to your Vietnamese relatives as a Singaporean memorabilia",
  avatar_base64: "[base64 of image]",
  avatar_filename: "hetcuu.png"
}
```
returns
```js
{
  status: "Updated successfully"
}
```
##### GET
```js
{
  full_name: "Yang Tuấn Anh",
  bio: "why would you buy a dragonfruit from Singapore just to show it off to your Vietnamese relatives as a Singaporean memorabilia",
  avatar: "[s3 link of image]"
}
```
#### `/profile/<int:user_id>`
Returns the profile of a specified user id.
##### GET
```js
{
  full_name: "Yang Tuấn Anh",
  bio: "why would you buy a dragonfruit from Singapore just to show it off to your Vietnamese relatives as a Singaporean memorabilia",
  avatar: "[s3 link of image]"
}
```
#### `/friends`
##### GET
Returns a list of user objects which are friends to the authenticated user.
#### `/friends/<int:user_id>`

##### GET
Returns a list of user objects which are friends to the user with given id.

##### POST
If not friended, then adds them onto the current users' friendlist, as well as using bipartite graph matching to add people with most common friends into a recommendation list. Returns:
```js
{
  "status": "Added friendship of User 12 with User 22"
}
```

Else, remove them from friendlist and recommended users who are friends of that person. Returns:
```js
{
  "status": "Removed friendship of User 12 with User 22"
}
```

#### `/friends/suggestions`
Returns 5 users sorted by most common friends, or select randomly if there isnt enough users to suggest by commonality.

### /posts
#### GET
#### POST
Login required. No input. If not friended, will add new connection between authenticated user and user with given user id. Else, then unfriend.
#### `/`
Returns current user's posts or submit new post.
##### GET
Returns
```js
[{
  id: 1,
  user: "yangtuananh2003",
  title: "Review cantin Sư Phạm",
  body: "ngon nhưng đông vl",
  rating: 5,
  username: "daothit",
  image_link: "[s3 link]",
  create_at: "[timedate]"
}, ...
]
```
##### POST
```js
{
  title: "Review cantin KHTN",
  body: "ngon qua", 
  rating: 5, 
  image_base64: "[base64 image]", 
  image_name: "khtn.png"
}
```
returns
```js
{
  status: "Created post 3743289"
}
```
#### `/<int:post_id>`
Returns post
##### GET
Returns
```js
{
  id: 1,
  user: "yangtuananh2003",
  title: "Review cantin Sư Phạm",
  body: "ngon nhưng đông vl",
  food_id: 123,
  rating: 5,
  image_link: "[s3 link]",
  create_at: "[timedate]"
}
```
Login required, only deletes posts that you made.

##### DELETE
```js
{
  status: "Deleted post 23493915"
}
```

#### `/reactions/<int:post_id>`
Returns reactions for a post
##### POST
No input, returns
```js
{
  status: "yangtuananh2003 reacted to 12375839"
}
```
if gave reaction, else if reacted
```js
{
  status: "Deleted reaction from 12375839"
}
```
##### GET
```js
{
  count: 100
}
```
#### `/reviews/<int:food_id>`
##### GET
Returns posts about that food item. Refer to `/<int:food_id>` for format.
### stores
### `/search-autocomplete`
Returns searched store
##### GET
```
  query: "buger"
  limit: "10"
```
Returns
```js
{
  status: "success",
  results: [
    {
        "name": "Cơm 42",
        "address": "42 Cô Bắc, Quận 1, TP. HCM",
        "latitude": 10.765162,
        "longitude": 106.69518
    },
    {
        "name": "Cơm 98",
        "address": "98 Lê Văn Lương, P. Tân Hưng, Quận 7, TP. HCM",
        "latitude": 10.7511547,
        "longitude": 106.7050986
    },
  ]
}
```
### `/<int:store_id>`
Returns store details
##### GET
Takes in `<int:store_id>`, returns:
```js
{
    "name": "Cơm 42",
    "address": "42 Cô Bắc, Quận 1, TP. HCM",
    "latitude": 10.765162,
    "longitude": 106.69518,
    "avg_rating": 4,
    "image_link": "https://images.foody.vn/res/g112/1112437/prof/s640x400/foody-upload-api-foody-mobile-se-5704914d-211022141924.jpeg"
}
```
##### POST
Takes in `<int:store_id>` and:
```js
{
  name: "Cơm tấm 3 miền",
  address: "123 Nguyễn Văn Cừ, phường 1, quận 5", 
  latitude: "80.223", 
  longitude: "102.1233"
}
```
Returns
```js
{
  status: "Created store + <int:store_id>"
}
```
##### PUT
Takes in `<int:store_id>` and:
```js
{
  name: "Cơm tấm 3 miền",
  address: "123 Nguyễn Văn Cừ, phường 1, quận 5", 
  latitude: "80.223", 
  longitude: "102.1233"
}
```
Returns
```js
{
  status: "Updated store + <int:store_id>"
}
```
##### DELETE
Takes in `<int:store_id>`, returns:
```js
{
  status: "Deleted store + <int:store_id>"
}
```
### feed
#### `\`
##### GET
Returns the first 50 posts sorted by newest
### food
### `/search-autocomplete`
Returns searched store
##### GET
```
  query: "cơm"
  limit: "10"
```
Returns
```js
{
  "status": "success",
  "results": [
    "cơm",
    "cơm",
    "cơm bì",
    "cơm thêm",
    "cơm bò úc",
    "cơm cá kho",
    "cơm bì chả",
    "cơm sườn bì chả",
    "cơm bò xào măng",
    "cơm ba rọi nướng"
  ]
}
```
### tags
#### `\`
##### GET
Takes in `query`, returns:
```js
{
  id: 1,
  title: "com_ga",
  store: 24653
}
```
##### POST
Creates a new tag, if it hasnt existed yet. Input takes in `query`, `longitude`, `latitude`. Returns:
```js
{
  status: "#com_ga was created with store $Dịch Vụ Đám Tiệc Ba Thu"
} 
```

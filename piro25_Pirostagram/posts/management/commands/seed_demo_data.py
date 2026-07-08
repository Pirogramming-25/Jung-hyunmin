# posts/management/commands/seed_demo_data.py
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from accounts.models import Follow, User
from posts.models import Post, PostImage, Story, StoryImage

DEMO_PASSWORD = 'testpass123!'

DEMO_USERS = [
    {'username': 'jihoon', 'name': '김지훈', 'bio': '사진 찍는 거 좋아합니다', 'avatar': 'fc4af7226a33ba82704ec3355438229465e91427.png'},
    {'username': 'minji', 'name': '박민지', 'bio': '여행 다니는 중', 'avatar': 'a2cdad3540b8112bf5190c4cd6dc2eeb5ff6550b.png'},
    {'username': 'seojun', 'name': '이서준', 'bio': '개발자 / 고양이 집사', 'avatar': '7b8b0ae94903f0525ba28eda685afb8721a8cbfc.png'},
    {'username': 'yuna', 'name': '최유나', 'bio': '', 'avatar': '6bdcb5620bc007c41f19be5e96463edc2b1a5ca4.png'},
]

POST_IMAGES = [
    '7e9aec13cc2f24f4179b0f4fd1e77ce9e9908247.png',
    '21375_feed_grid_photo.png',
    'b033b4ff8cedf06cdae6ccb05d90e339f8342eef.png',
    '48eaffdce4986e5a70387445632a994d206fb0a5.png',
]

CAPTIONS = ['오늘 하루도 화이팅!', '점심 뭐 먹지 고민중', '주말 나들이 다녀왔어요', '새로운 취미 시작!']


class Command(BaseCommand):
    help = '브라우저 테스트용 데모 유저/게시글/스토리/팔로우 데이터를 생성합니다.'

    def handle(self, *args, **options):
        assets_dir = settings.BASE_DIR / 'static' / 'assets'
        users = []

        for info in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=info['username'],
                defaults={'name': info['name'], 'bio': info['bio']},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                with open(assets_dir / info['avatar'], 'rb') as f:
                    user.profile_image.save(info['avatar'], File(f), save=False)
                user.save()
                self.stdout.write(f'유저 생성: {info["username"]} / {DEMO_PASSWORD}')
            users.append(user)

        for i, user in enumerate(users):
            if user.posts.exists():
                continue
            for j in range(2):
                post = Post.objects.create(author=user, caption=CAPTIONS[(i + j) % len(CAPTIONS)])
                image_name = POST_IMAGES[(i + j) % len(POST_IMAGES)]
                post_image = PostImage(post=post, order=0)
                with open(assets_dir / image_name, 'rb') as f:
                    post_image.image.save(image_name, File(f), save=False)
                post_image.save()
            self.stdout.write(f'{user.username}의 게시글 2개 생성')

        for i, user in enumerate(users):
            target = users[(i + 1) % len(users)]
            Follow.objects.get_or_create(follower=user, following=target)

        first_user = users[0]
        if not first_user.stories.exists():
            story = Story.objects.create(author=first_user)
            avatar_name = DEMO_USERS[0]['avatar']
            story_image = StoryImage(story=story, order=0)
            with open(assets_dir / avatar_name, 'rb') as f:
                story_image.image.save(avatar_name, File(f), save=False)
            story_image.save()
            self.stdout.write(f'{first_user.username}의 스토리 생성')

        self.stdout.write(self.style.SUCCESS('데모 데이터 생성 완료'))

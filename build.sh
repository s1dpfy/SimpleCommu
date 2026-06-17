
set -o errexit

echo "라이브러리 설치 중..."
pip install -r requirements.txt

echo "정적 파일 모으는 중..."
python manage.py collectstatic --no-input

echo "데이터베이스 마이그레이션 중..."
python manage.py migrate

echo "관리자 계정 자동 생성 중..."
python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'); password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '12345678'); u, created = User.objects.get_or_create(username=username); u.set_password(password); u.is_superuser = True; u.is_staff = True; u.save(); print('세팅되었습니다!')"
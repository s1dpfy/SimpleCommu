
set -o errexit

echo "라이브러리 설치 중..."
pip install -r requirements.txt

echo "정적 파일 모으는 중..."
python manage.py collectstatic --no-input

echo "데이터베이스 마이그레이션 중..."
python manage.py migrate
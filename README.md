# demo-v1fs (update the app.py file adding your API KEY)

git clone https://github.com/andrefernandes86/demo-v1fs.git

cd demo-v1fs

docker buildx create --use

for amd64: docker buildx build --platform linux/amd64 -t demo-v1fs --load .

or for arm64: docker buildx build --platform linux/arm64 -t demo-v1fs --load .

docker run -it -p 80:5000 demo-v1fs

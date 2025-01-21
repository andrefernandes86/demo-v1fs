# demo-v1fs

git clone https://github.com/andrefernandes86/demo-v1fs.git

cd demo-v1fs

docker build -t demo-v1fs .

docker run -it -p 80:5000 demo-v1fs

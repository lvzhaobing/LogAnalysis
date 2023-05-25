docker run -d \
  --name=qde_desktop \
  --security-opt seccomp=unconfined \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e SUBFOLDER=/ \
  -e TITLE=QDE \
  -p 3000:3000 \
  -p 3001:3001 \
  -p 5000:5000 \
  -p 5001:5001 \
  -v /home/$USER/ide-7.1-workspace:/config/ide-7.1-workspace \
  -v $(pwd)/../bin/Release/net6.0/publish:/config/publish \
  -v $(pwd)/../wwwroot/analysis_kev/:/config/publish/wwwroot/analysis_kev \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --device /dev/dri:/dev/dri \
  --shm-size="1gb" \
  --restart unless-stopped \
  ubuntu_desktop:v1.0 
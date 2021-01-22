import qbittorrentapi
import json
with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()
QB_host=conf["QB_host"]
QB_port=conf["QB_port"]
QB_username=conf["QB_username"]
QB_password=conf["QB_password"]

def del_torrent(hash):
# instantiate a Client using the appropriate WebUI configuration
    qbt_client = qbittorrentapi.Client(host=QB_host, port=QB_port, username=QB_username, password=QB_password)
    result=qbt_client.torrents_delete(delete_files=True,torrent_hashes=hash)

'''# the Client will automatically acquire/maintain a logged in state in line with any request.
# therefore, this is not necessary; however, you many want to test the provided login credentials.


# display qBittorrent info
print(f'qBittorrent: {qbt_client.app.version}')
print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
for k,v in qbt_client.app.build_info.items(): print(f'{k}: {v}')

# retrieve and show all torrents
for torrent in qbt_client.torrents_info(torrent_hashes = "6b7731d1838a2b69c2fb82406ad912c17f29fa4f"):
    print(f'{torrent.hash[-6:]}: {torrent.name} ({torrent.state})')

#添加标签
qbt_client.torrents_add_tags(tags="test",torrent_hashes = "6b7731d1838a2b69c2fb82406ad912c17f29fa4f")

#获取单个种子的信息
print(qbt_client.torrents_info(torrent_hashes = "6b7731d1838a2b69c2fb82406ad912c17f29fa4f")[0])
torrent=qbt_client.torrents_info(torrent_hashes = "6b7731d1838a2b69c2fb82406ad912c17f29fa4f")[0]
print(f'{torrent.hash[-6:]}: {torrent.name} ({torrent.state})')'''

#64f22355dd2b7f114f833da8dd8fdd0eb3fa0305


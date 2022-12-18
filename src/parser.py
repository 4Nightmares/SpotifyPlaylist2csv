#!/usr/bin/env python
if __name__ == "__main__":
    import urllib3
    from bs4 import BeautifulSoup
    import re, argparse
    
    parser = argparse.ArgumentParser(description="Spotify Playlist to CSV",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", help="https://open.spotify.com/embed/playlist/... or https://open.spotify.com/playlist/...")
    args = parser.parse_args()
    
    http = urllib3.PoolManager()
    x = re.compile("^https:\/\/open\.spotify\.com(?:\/embed)?\/playlist/([a-z,A-Z,0-9]*)$")
    y = x.match(args.url)
    if y:
        r = http.request("GET", F"https://open.spotify.com/embed/playlist/{y.group(1)}")
        if r.status == 200:
            soup = BeautifulSoup(r.data, "html.parser")
        
            title, user = soup.find("h1").get_text(), soup.find("h2").get_text()
            filename = F"{title} - {user}.csv"
        
            with open(filename, "w") as f:
                for track, artist in zip(soup.find_all("h3"),soup.find_all("h4")):
                    f.write(F'"{track.get_text()}","{artist.get_text()}"\n')
            
            print(filename)
        else:
            print("Bad Playlist")
    else:
        print("Bad URL")

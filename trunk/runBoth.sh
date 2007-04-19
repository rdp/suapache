nohup ./run_forever.sh "python establishAlien.py " >> /home/byu_p2pweb/logs/nothing.establishAlien.py.out.runBoth.nothing &
nohup ./run_forever.sh "python proxyServer.py 3220 10005 8000" >> /home/byu_p2pweb/logs/nothing.proxyServer.py.3220.out.runBoth.nothing &
nohup ./run_forever.sh "python proxyServer.py 3221 10006 8001"  >> /home/byu_p2pweb/logs/nothing.proxyServer.py.3221.out.runBoth.nothing &
nohup ./run_forever.sh "python proxyServer.py 3222 10007 8002"  >> /home/byu_p2pweb/logs/nothing.proxyServer.py.3222.out.runBoth.nothing &


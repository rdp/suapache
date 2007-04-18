nohup ./run_forever.sh "python establishAlien.py " >> nothing.establishAlien.py.out.runBoth.nothing &
nohup ./run_forever.sh "python proxyServer.py 3220 10005 8000" >> nothing.proxyServer.py.out.runBoth.nothing &
#python proxyServer.py 3222 10006 8001
nohup ./run_forever.sh "python proxyServer.py 3221 10006 8001"  >> nothing.proxyServer.py.out.runBoth.nothing &
nohup ./run_forever.sh "python proxyServer.py 3222 10007 8002"  >> nothing.proxyServer.py.out.runBoth.nothing &


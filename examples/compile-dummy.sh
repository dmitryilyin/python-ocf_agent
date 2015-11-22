rm -f dummy.c dummy dummy.o
cython --embed -o dummy.c dummy.py
gcc -pthread -c dummy.c -I/usr/include/python2.7 -I/usr/include/python2.7
gcc -pthread -o dummy dummy.o -L/usr/lib -L/usr/lib/python2.7/config-x86_64-linux-gnu -lpython2.7 -lpthread -ldl  -lutil -lm -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions

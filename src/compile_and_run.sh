if [ "$1" != "--debug" ]; then
#     java -cp .:postgresql.jar:dropbox-sdk-java-5.1.1.jar:jackson-core-2.7.9.jar Coffee
    javac -cp .:lib/* Coffee.java && java -cp .:lib/* Coffee
else
#     java -cp .:postgresql.jar:dropbox-sdk-java-5.1.1.jar:jackson-core-2.7.9.jar Coffee --debug
    javac -cp .:lib/* Coffee.java && java -cp .:lib/* Coffee --debug
fi
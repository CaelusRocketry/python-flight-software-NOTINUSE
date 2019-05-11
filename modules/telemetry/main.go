package telemetry

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

// only needed below for sample processing
var IP = "192.168.1.170:8081"

func TestServer() {

	fmt.Println("Launching server...")

	// listen on all interfaces
	ln, _ := net.Listen("tcp", IP)

	fmt.Println("Listening")

	// accept connection on port
	conn, _ := ln.Accept()

	fmt.Println("Connected")

	// run loop forever (or until ctrl-c)
	for {
		// will listen for message to process ending in newline (\n)
		message, _ := bufio.NewReader(conn).ReadString('\n')
		// output message received
		fmt.Print("Message Received:", string(message))
		// sample process for string received
		message = Ingest(message)
		// send new string back to client
		conn.Write([]byte(message + "\n"))
	}
}

func TestClient() {

	// connect to this socket
	conn, _ := net.Dial("tcp", IP)
	for {
		// read in input from stdin
		fmt.Println("Client hello")
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Text to send: ")
		text, _ := reader.ReadString('\n')
		// send to socket
		fmt.Fprintf(conn, text+"\n")
		// listen for reply
		message, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Print("Message from server: " + message)
	}
}

func Listen() {
	fmt.Println("Hey testing Listen")
}

func Send() {
	fmt.Println("hey testing send")
}

/*
corresponding code in Python:

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.84', 8081))

*/

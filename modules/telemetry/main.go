package telemetry

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

var IP = "127.0.0.1:8081" // Needed for local development
var QUEUE []string        // Client -> server queue
var OUTQUEUE []string     // Server -> client queue

func TestServer() {
	fmt.Println("Launching server...")

	ln, _ := net.Listen("tcp", IP) // Listen on all interfaces

	fmt.Println("Listening")

	conn, _ := ln.Accept() // Accept connection on port

	fmt.Println("Connected")
	go listenStuff(conn)
	go sendStuff(true, conn)
	reader := bufio.NewReader(os.Stdin)
	a := ""
	for a != "ABORT" {
		a, _ = reader.ReadString('\n')
		a = strings.Replace(a, "\n", "", -1)
		Outqueue("GS", a)
	}
}

func listenStuff(conn net.Conn) {
	fmt.Println("Doing stuff")

	for {
		message, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Println("Message Received:", string(message))
		var pack Packet
		json.Unmarshal([]byte(message), &pack)
		message = Ingest(pack)
		if message == "ABORT" {
			fmt.Println("ABORTING NOW, GLHF")
			return
		}
	}
}

func sendStuff(isServer bool, conn net.Conn) {
	if isServer {
		for {
			if len(OUTQUEUE) > 0 {
				msg := OUTQUEUE[0]
				if isServer {
					conn.Write([]byte(msg + "\n"))
				} else {
					fmt.Fprintf(conn, msg+"\n")
				}
				OUTQUEUE = OUTQUEUE[1:]
			}
		}
	} else {
		for {
			if len(QUEUE) > 0 {
				msg := QUEUE[0]
				if isServer {
					conn.Write([]byte(msg + "\n"))
				} else {
					fmt.Fprintf(conn, msg+"\n")
				}
				QUEUE = QUEUE[1:]
			}
		}
	}
}
func TestClient() {
	// Connect to this socket
	conn, _ := net.Dial("tcp", IP)
	fmt.Println("Client connected")

	go sendStuff(false, conn)
	go listenStuff(conn)

	for {
		Enqueue("abc", "Temp")
		time.Sleep(500 * time.Millisecond)
		Enqueue("abc", "Pressure")
		time.Sleep(500 * time.Millisecond)
	}
	//	for {
	//		reader := bufio.NewReader(os.Stdin)
	//		fmt.Print("Text to send: ")
	//		text, _ := reader.ReadString('\n')
	// send to socket

	//		fmt.Fprintf(conn, text+"\n")
	// listen for reply
	//		message, _ := bufio.NewReader(conn).ReadString('\n')
	//		fmt.Print("Message from server: " + message)
	//	}
}

func Listen() {
	fmt.Println("Testing Listen()")
}

func Send() {
	fmt.Println("Testing Send()")
}

/*
corresponding code in Python:

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.84', 8081))

*/

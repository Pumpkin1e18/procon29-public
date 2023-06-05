using UnityEngine;
using System;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.IO;
using System.Text;
using System.Net;

public class Chat : MonoBehaviour {
	private List<string> messages = new List<string>();
	private string currentMessage = string.Empty;
	// Server
	NetworkStream stream = null;
	bool isStopReading = false;
	byte[] readbuf;

	public void SendCommand(string str){
		StartCoroutine (SendMessage(str));
	}

	private IEnumerator Start(){
		Debug.Log("START START");
		readbuf = new byte[2048];
		float start_time = Time.realtimeSinceStartup;

		while (true) {
			if (Time.realtimeSinceStartup-start_time >= 5) {
				//StartCoroutine (SendMessage ("Hello,Server!"));
				start_time = Time.realtimeSinceStartup;
			}
			if (!isStopReading) StartCoroutine (ReadMessage ());
			yield return null;
		}
	}

	private IEnumerator SendMessage(string message){
		Debug.Log ("START SendMessage:" + message);
		if (stream == null) {
			stream = GetNetworkStream();
		}
		string playerName = "[FromUnity]: ";
		Encoding enc = Encoding.UTF8;
		byte[] sendBytes = enc.GetBytes(playerName + message + "\n");
		stream.Write(sendBytes, 0, sendBytes.Length);
		//Debug.Log ("Send Message: "+sendBytes);
		yield break;
	}

	private IEnumerator ReadMessage(){
		stream = GetNetworkStream ();
		stream.BeginRead (readbuf, 0, readbuf.Length, new AsyncCallback (ReadCallback), null);
		isStopReading = true;
		yield return null;
	}

	public void ReadCallback(IAsyncResult ar){
		Encoding enc = Encoding.UTF8;
		stream = GetNetworkStream ();
		int bytes = stream.EndRead(ar);
		string message = enc.GetString (readbuf, 0, bytes);
		message = message.Replace("\r", "").Replace("\n", "");//
		Debug.Log (message);
		if(message[5] == 'P')FieldCreate.str = message;
		isStopReading = false;
		//messages.Add(message);
	}   

	private NetworkStream GetNetworkStream(){
		if (stream != null && stream.CanRead) {
			return stream;
		}
		string ipOrHost = "127.0.0.1";
		int port = 10021;
		TcpClient tcp = new TcpClient(ipOrHost, port);
		Debug.Log("success connect server");
		return tcp.GetStream();
	}

	private Socket GetSocket(){
		IPAddress ipAddress = IPAddress.Parse("127.0.0.1");
		IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 10021);
		Socket listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp );
		listener.Bind(localEndPoint);
		listener.Listen(10);
		return listener;
	}
}

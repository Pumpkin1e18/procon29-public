using System;
using System.Threading;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Text;
using System.Collections.Generic;

namespace Server{
    class MainClass{
        public static Dictionary<TcpClient, int> clientDict = new Dictionary<TcpClient, int>();

        public static void Main (string[] args){
            Console.WriteLine ("START");
            // 非同期でチャットルームを立ち上げる
            Task.Run (() => ChatRoom ("room name"));

            // TCPサーバを立ち上げる
            string ipString = "127.0.0.1";
            System.Net.IPAddress ipAdd = System.Net.IPAddress.Parse(ipString);
            //Listenするポート番号
            int port = 10021;

            //TcpListenerオブジェクトを作成する
            TcpListener server = new TcpListener(ipAdd, port);

            //Listenを開始する
            server.Start();
            Console.WriteLine("Listenを開始しました({0}:{1})。",
                ((System.Net.IPEndPoint)server.LocalEndpoint).Address,
                ((System.Net.IPEndPoint)server.LocalEndpoint).Port);

            // test
            Task.Run(()=>TestChat());


            while (true) {
                //接続要求があったら受け入れる
                TcpClient client = server.AcceptTcpClient ();

                //クライアントからのTCP接続は別スレッドに投げる
                Task.Run(() => ChatStream(client));
            }

            Console.WriteLine ("FINISH");
        }

        static void ChatRoom(string tag){
            Console.WriteLine ("Start Chat");
            Console.WriteLine ("Finish Chat");
        }

        static async Task ChatStream(TcpClient client){
            Console.WriteLine ("クライアント({0}:{1})と接続しました。",
                ((IPEndPoint)client.Client.RemoteEndPoint).Address,
                ((IPEndPoint)client.Client.RemoteEndPoint).Port);

            clientDict.Add (client, 0);

            //NetworkStreamを取得
            NetworkStream stream = client.GetStream ();
            StreamReader reader = new StreamReader (stream);


            //接続されている限り読み続ける
            while (client.Connected) {
                //Console.WriteLine("receiving...");
                string line = await reader.ReadLineAsync () + '\n';
                if(line == "\n")break; //接続が切れるとループを抜ける
                Console.WriteLine ("Message:" + line);

                // bloadcastで接続しているclient全員に通知
                Task.Run(()=>Broadcast(line));
            }
            clientDict.Remove (client);
            Console.WriteLine("クライアントとの接続が切れました");
        }

        static async Task Broadcast(string message){
            if (System.String.IsNullOrEmpty(message)){
                return;
            }

            foreach (KeyValuePair<TcpClient, int> pair in clientDict) {
                if (pair.Key.Connected) {
                    NetworkStream stream = pair.Key.GetStream ();
                    await stream.WriteAsync (Encoding.ASCII.GetBytes(message), 0, message.Length);
                    //Console.WriteLine ("Send Done:" + message);
                }
            }
        }


        static async Task TestChat(){
            Task.Delay(1000);
            Console.WriteLine ("-Start TestChat");

            // 接続試験
            string ipOrHost = "127.0.0.1";
            int port = 10021;
            TcpClient client = new TcpClient(ipOrHost, port);
            var stream = client.GetStream();

            // 送信
            Thread.Sleep(1000);
            Encoding enc = Encoding.UTF8;
            byte[] sendBytes = enc.GetBytes("test message" + '\n');
            //データを送信する
            stream.Write(sendBytes, 0, sendBytes.Length);

            // 受信
            Console.WriteLine ("--Start Read");
            StreamReader reader = new StreamReader (stream);
            string line = await reader.ReadLineAsync ();
            Console.WriteLine ("-TestChat Message:" + line);
            Console.WriteLine ("-Finish TestChat");

            // 定期送信試験
            /*int count = 0;
            while (true) {
                sendBytes = enc.GetBytes("[FromServer]: time send" + count.ToString() + '\n');
                //データを送信する
                stream.Write(sendBytes, 0, sendBytes.Length);
                //Thread.Sleep(5000);
                await Task.Delay(5000);
                count++;
            }*/
        }
    }
}


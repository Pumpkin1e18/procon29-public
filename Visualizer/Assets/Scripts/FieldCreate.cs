using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;

//Create Field and process the command from Python
public class FieldCreate : MonoBehaviour {

	public GameObject obj;
	public GameObject obj2;
	public static int selectPlayer = -1;
	public static int h = 8, w = 11;
	public static int[] score = new int[2];
	public static int[] playerY = new int[4];
	public static int[] playerX = new int[4];
	public static int[] posMove = new int[4] {-1, -1, -1, -1};
	public static int[] posBool = new int[4] {0, 0, 0, 0};
	public static int[] vecMove = new int[4] {-1, -1, -1, -1};
	public static int[] vecBool = new int[4] {0, 0, 0, 0};
	public static string str = "";
	public static int[,] board = new int[20,20];
	public static GameObject[,] number = new GameObject[20,20];
	public static GameObject[,] boxes = new GameObject[20,20];
	public static GameObject[] sm = new GameObject[9];

	//create test board
	void Start () {
		Debug.Log ("Created test board");
		for (int i = 0; i < h; i++) {
			for (int j = 0; j < w; j++) {
				boxes[i,j] = Instantiate (obj, new Vector2 (0, 0), Quaternion.identity);
				boxes[i,j].transform.SetParent (this.transform);
				boxes[i,j].transform.position = new Vector2 (j, -i);
				boxes[i,j].name = "Box" + (i*w+j).ToString ();
				number[i,j] = boxes[i,j].transform.GetChild (0).gameObject;
				int x = (i*w+j)%10;
				number[i,j].GetComponent<TextMesh>().text = x.ToString();
			}
		}
		Chat chat = GetComponent<Chat> ();
		chat.SendCommand ("init!");
	}

	public void selectMove(string str, int Bool){
		int h = FieldCreate.h, w = FieldCreate.w;
		bool banMove = false;
		if (playerY [selectPlayer] + (str [9] - '0')/3-1 < 0)banMove = true;
		if (playerY [selectPlayer] + (str [9] - '0')/3-1 >= h)banMove = true;
		if (playerX [selectPlayer] + (str [9] - '0')%3-1 < 0)banMove = true;
		if (playerX [selectPlayer] + (str [9] - '0')%3-1 >= w)banMove = true;
		if (banMove == true) {
			Debug.Log ("out of board");
			return;
		}
		Chat chat = GetComponent<Chat> ();
		posMove[selectPlayer] = str[9]-'0';
		posBool [selectPlayer] = Bool;
		selectPlayer = -1;
	}

	public void selectStart(string str){
		int length = str.Length, num = 0;
		for (int i = 3; i < length; i++) {
			num = num*10+(str[i]-'0');
		}
		int y = num / w, x = num % w;
		selectPlayer = -1;
		for (int i = 0; i < 4; i++) {
			if (y == playerY [i] && x == playerX [i])selectPlayer = i;
		}
		if (selectPlayer == -1)return;
		for (int i = 0; i < 9; i++) {
			int yy = y+((i/3)-1), xx = x+((i%3)-1);
			if(yy < 0 || yy >= h || xx < 0 || xx >= w)continue;
			sm[i] = Instantiate (obj2, new Vector2 (0, 0), Quaternion.identity);
			sm[i].transform.position = new Vector2 (xx, -yy);
			sm[i].name = "SelectGUI" + i.ToString();
		}
	}

	//process the command from Python
	void Update () {
		//int length = str.Length, cnt = 0, p = 16;
		//ex) [FromPython]: 1 0 2 2 1
		strAnalyze analysis = GetComponent<strAnalyze>();
		//if (str != "" && str [5] == 'P')Debug.Log (str);
		//if(str != "")Debug.Log(str);
		if (str != "" && str [5] == 'P' && str [14] == '0') analysis.Init(str);
		if (str != "" && str [5] == 'P' && str [14] == '1') analysis.boardDisp (str);
		if (str != "" && str [5] == 'P' && str [14] == '2') analysis.vectorDisp (str);
		str = "";
		analysis.applyBoard ();
	}

}

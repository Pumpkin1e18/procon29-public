using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerInfo : MonoBehaviour {

	GameObject selectPlayer;
	GameObject selectText;
	GameObject[] playerInfo = new GameObject[2];
	GameObject[] infoText = new GameObject[2];
	string[] infoState = new string[4];

	void Start () {
		playerInfo [0] = GameObject.Find ("PlayerInfo(Red)");
		playerInfo [1] = GameObject.Find ("PlayerInfo(Blue)");
		infoText [0] = playerInfo [0].transform.GetChild (0).gameObject;
		infoText [1] = playerInfo [1].transform.GetChild (0).gameObject;
		selectPlayer = GameObject.Find ("SelectPlayer");
		selectText = GameObject.Find ("SelectPlayerText");
	}
	
	void Update () {
		int h = FieldCreate.h, w = FieldCreate.w;
		playerInfo[0].transform.position = new Vector2 (w+3, -(h/2));
		playerInfo[1].transform.position = new Vector2 (-4, -(h/2));
		for (int i = 0; i < 4; i++) {
			if (FieldCreate.posMove [i] == -1)infoState [i] = "?";
			else {
				infoState [i] = FieldCreate.posMove [i].ToString () + " ";
				infoState [i] += FieldCreate.posBool [i].ToString ();
			}
		}
		string redStr = "Player Red\nplayer1: " + infoState [0] + "\nplayer2: " + infoState[1];
		string blueStr = "Player Blue\nplayer3: " + infoState[2] + "\nplayer4: " + infoState[3];
		infoText[0].GetComponent<TextMesh>().text = redStr;
		infoText[1].GetComponent<TextMesh>().text = blueStr;
		int tmp = FieldCreate.selectPlayer+1;
		selectPlayer.transform.position = new Vector2 (w/2, 1.5f);
		if(tmp == 0)selectText.GetComponent<TextMesh> ().text = "";
		else selectText.GetComponent<TextMesh> ().text = "[Player" + tmp.ToString() + "]";
	}
}

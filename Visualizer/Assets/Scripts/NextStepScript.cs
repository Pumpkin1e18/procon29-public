using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;	//<-Watch out!

public class NextStepScript : MonoBehaviour {

	Button btn;
	GameObject field;
	public static int turnCount = 1;

	void Start () {
		btn = GetComponent<Button> ();
		btn.interactable = false;
		field = GameObject.Find ("Field");
	}

	public void OnClick(){
		Debug.Log ("pushed Next Step");
		GameObject tmp = GameObject.Find ("Field");
		strAnalyze analysis = tmp.GetComponent<strAnalyze>();
		turnCount += 1;
		btn.interactable = false;
		string str = "0 ";
		for (int i = 0; i < 4; i++) {
			str += FieldCreate.posMove [i].ToString () + " ";
			str += FieldCreate.posBool [i].ToString () + " ";
			FieldCreate.posMove [i] = -1;
			FieldCreate.vecMove[i] = -1;
			analysis.destroy (i);
		}
		Chat chat = field.GetComponent<Chat>();
		chat.SendCommand (str);
	}

	void Update () {
		bool flag = true;
		for (int i = 0; i < 4; i++) {
			if (FieldCreate.posMove [i] == -1)flag = false;
		}
		if (flag)btn.interactable = true;
	}
}

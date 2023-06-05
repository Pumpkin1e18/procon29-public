using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;	//<-Watch out!

public class PrevScript : MonoBehaviour {

	Button btn;
	GameObject field;

	void Start () {
		btn = GetComponent<Button> ();
		field = GameObject.Find ("Field");
	}

	public void OnClick(){
		Debug.Log ("pushed Prev Button");
		NextStepScript.turnCount -= 1;
		string str = "3 ";
		Chat chat = field.GetComponent<Chat>();
		chat.SendCommand (str);
	}

	void Update () {
		if(NextStepScript.turnCount == 1)btn.interactable = false;
		else btn.interactable = true;
	}
}

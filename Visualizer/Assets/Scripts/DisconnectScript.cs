using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisconnectScript : MonoBehaviour {

	Button btn;
	GameObject field;

	void Start () {
		btn = GetComponent<Button> ();
		btn.interactable = true;
		//btn.interactable = false;
		field = GameObject.Find ("Field");
	}

	public void OnClick(){
		Debug.Log ("Disconnected");
		NextStepScript.turnCount = 1;
		Chat chat = field.GetComponent<Chat>();
		chat.SendCommand ("1 ");
		//strAnalyze.initFlag = false;
	}
	
	void Update () {
		//if(strAnalyze.initFlag)btn.interactable = true;
		//else btn.interactable = false;
	}
}

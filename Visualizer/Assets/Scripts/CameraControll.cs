using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControll : MonoBehaviour {
	
	float size = 10;
	private Camera cam;
	bool moveFlag = false;
	bool[] getKey = new bool[2];
	private Vector2 lastMousePosition;
	private Vector2 MousePosition;

	void Start () {
		cam = GetComponent<Camera>();
	}

	//If object doesn't have collider2D, return null
	private GameObject getClickObject() {
		GameObject result = null;
		getKey [0] = Input.GetMouseButtonDown (0);
		getKey [1] = Input.GetMouseButtonDown (1);
		if(getKey[0] || getKey[1]) {
			Vector2 tapPoint = Camera.main.ScreenToWorldPoint(Input.mousePosition);
			Collider2D collition2d = Physics2D.OverlapPoint(tapPoint);
			if (collition2d) {
				result = collition2d.transform.gameObject;
			}
			for (int i = 0; i < 9; i++)Destroy (FieldCreate.sm[i]);
		}
		return result;
	}

	void opKey(){	//operation for keyboard
		GameObject tmp = GameObject.Find ("Field");
		FieldCreate fc = tmp.GetComponent<FieldCreate>();
		string[] keyStr = {"qweasdzxc", "rtyfghvbn"};	//move 9 directions
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 9; j++) {
				if (FieldCreate.selectPlayer == -1)continue;
				if (Input.GetKeyDown (keyStr[i][j].ToString())) {
					//Debug.Log (keyStr[i][j]);
					fc.selectMove ("SelectGUI"+j.ToString(), i);
					FieldCreate.selectPlayer = -1;
					for (int k = 0; k < 9; k++)Destroy (FieldCreate.sm[k]);
				}
			}
		}
		if (Input.GetKeyDown ("return")) {		//Next Step
			tmp = GameObject.Find ("NextStepButton");
			NextStepScript nextstep = tmp.GetComponent<NextStepScript>();
			nextstep.OnClick ();
		}
		if (Input.GetKeyDown ("space")) {		//Time Set
			Debug.Log ("Time Set");
			ScoreScript.timeFloat = 0;
		}
		if (Input.GetKeyDown (KeyCode.Keypad7)) {	//player1
			FieldCreate.selectPlayer = -1;
			for (int k = 0; k < 9; k++)Destroy (FieldCreate.sm[k]);
			int pos = FieldCreate.playerY[0] * FieldCreate.w + FieldCreate.playerX[0];
			fc.selectStart ("Box"+pos.ToString());
		}
		if (Input.GetKeyDown (KeyCode.Keypad9)) {	//player2
			FieldCreate.selectPlayer = -1;
			for (int k = 0; k < 9; k++)Destroy (FieldCreate.sm[k]);
			int pos = FieldCreate.playerY[1] * FieldCreate.w + FieldCreate.playerX[1];
			fc.selectStart ("Box"+pos.ToString());
		}
		if (Input.GetKeyDown (KeyCode.Keypad1)) {	//player3
			FieldCreate.selectPlayer = -1;
			for (int k = 0; k < 9; k++)Destroy (FieldCreate.sm[k]);
			int pos = FieldCreate.playerY[2] * FieldCreate.w + FieldCreate.playerX[2];
			fc.selectStart ("Box"+pos.ToString());
		}
		if (Input.GetKeyDown (KeyCode.Keypad3)) {	//player4
			FieldCreate.selectPlayer = -1;
			for (int k = 0; k < 9; k++)Destroy (FieldCreate.sm[k]);
			int pos = FieldCreate.playerY[3] * FieldCreate.w + FieldCreate.playerX[3];
			fc.selectStart ("Box"+pos.ToString());
		}
		if (Input.GetKeyDown (KeyCode.Keypad5)) {	//cancel
			FieldCreate.selectPlayer = -1;
			for (int k = 0; k < 9; k++)Destroy (FieldCreate.sm[k]);
		}
	}

	void Update (){
		float fWheel = Input.GetAxis("Mouse ScrollWheel"); 
		transform.Translate(0, 0, fWheel);
		size -= 2.0f*fWheel;
		cam.orthographicSize = size;


		opKey ();	//operation for keyboard
		GameObject obj = getClickObject ();		//get click object
		if (Input.GetMouseButtonDown(0) && obj == null)FieldCreate.selectPlayer = -1;
		if (obj != null) {
			moveFlag = false;
			Debug.Log (obj.name);
			GameObject tmp = GameObject.Find ("Field");
			FieldCreate fc = tmp.GetComponent<FieldCreate>();
			if (obj.name [0] != 'S')FieldCreate.selectPlayer = -1;
			if (obj.name [0] == 'B' && getKey[0])		//Box
				fc.selectStart (obj.name);
			if (obj.name [0] == 'S' && getKey [0])		//SelectGUI(Left Click)
				fc.selectMove (obj.name, 0);
			else if (obj.name [0] == 'S' && getKey [1])	//SeectGUI(Right Click)
				fc.selectMove (obj.name, 1);
		}
		if (Input.GetMouseButtonDown(0) && obj == null) {
			moveFlag = true;
			lastMousePosition = Input.mousePosition;
		}else if (Input.GetMouseButton (0) && moveFlag == true) {
			MousePosition = Input.mousePosition;
			float xx = this.transform.position.x-0.05f*(MousePosition.x-lastMousePosition.x);
			float yy = this.transform.position.y-0.05f*(MousePosition.y-lastMousePosition.y);
			lastMousePosition.x = MousePosition.x;
			lastMousePosition.y = MousePosition.y;
			transform.position = new Vector3 (xx, yy, -10.0f);
		}

	}
}

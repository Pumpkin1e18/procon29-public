using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//Analyze string from Python
public class strAnalyze : MonoBehaviour {

	public GameObject obj;
	public GameObject VectorObj;
	public GameObject CircleObj;
	public static GameObject[] vectors = new GameObject[4];
	public static GameObject[] putCircle = new GameObject[4];
	public static bool initFlag = false;

	string str = "";
	int p = 0;
	int get_num(){
		string s = "";
		while(true){
			if (str[p] == ' ')break;
			s += str[p];p++;
		}p++;
		return int.Parse(s);
	}

	public void Init(string s){			//[FromPython]: 0 h w number[h*w] pos[4]
		//ScoreScript.timeFloat = 0;
		NextStepScript.turnCount = 1;
		str = s;p = 16;
		//if(initFlag == true)return;
		//initFlag = true;
		Debug.Log ("Called Init");
		Debug.Log (str);
		int length = str.Length, cnt = 0;
		int h = get_num ();
		int w = get_num ();
		FieldCreate.h = h;FieldCreate.w = w;
		for (int i = 0; i < 20; i++) {
			for(int j = 0;j < 20;j++)Destroy(FieldCreate.boxes[i, j]);
		}
		//get board number
		while(true) {
			int y = cnt / w, x = cnt % w;
			//Destroy(FieldCreate.boxes[y, x]);
			FieldCreate.boxes[y,x] = Instantiate (obj, new Vector2 (0, 0), Quaternion.identity);
			FieldCreate.boxes[y,x].transform.SetParent (this.transform);
			FieldCreate.boxes[y,x].transform.position = new Vector2 (x, -y);
			FieldCreate.boxes [y, x].name = "Box" + cnt.ToString ();
			FieldCreate.number[y,x] = FieldCreate.boxes[y,x].transform.GetChild (0).gameObject;
			int num = get_num ();
			FieldCreate.number[y,x].GetComponent<TextMesh>().text = num.ToString();
			cnt++;if (cnt == h * w)break;
		}
		//get player pos
		Debug.Log (str);
		for (int i = 0; i < 4; i++) {
			int num = get_num ();
			FieldCreate.playerY [i] = num;
			num = get_num ();
			FieldCreate.playerX [i] = num;
		}
	}

	public void boardDisp (string s){			//[FromPython]: 1 color[h*w] pos[4] score[2]
		Debug.Log(str);
		str = s;p = 16;
		int length = str.Length, cnt = 0;
		int h = FieldCreate.h, w = FieldCreate.w;
		//get board color
		while (true) {
			int num = get_num ();
			FieldCreate.board [cnt / w, cnt % w] = num;
			cnt++;if (cnt == h * w)break;
		}
		//get player pos
		for (int i = 0; i < 4; i++) {
			int num = get_num ();
			FieldCreate.playerY [i] = num;
			num = get_num ();
			FieldCreate.playerX [i] = num;
		}
		//get score(red and blue)
		for (int i = 0; i < 2; i++) {
			int num = get_num ();
			FieldCreate.score [i] = num;
			ScoreScript.scoreInt[i] = num;
		}
	}

	public void vectorDisp (string s){	//[FromPython]: 2 [[v1[i], b1[i], ...]
		str = s;p = 16;
		//Debug.Log (str);
		for (int i = 0; i < 4; i++) {
			float[] dv = new float[9] {45f, 0f, -45f, 90f, 0f, -90f, 135f, 180f, -135f};
			int y = FieldCreate.playerY[i], x = FieldCreate.playerX[i];
			int m = get_num (), b = get_num ();
			FieldCreate.vecMove [i] = m;
			FieldCreate.vecBool [i] = b;
			Destroy(vectors[i]);
			if (m == -1 || m == 4) continue;
			float yy = (float)y+(float)(m/3-1)*0.5f;
			float xx = (float)x+(float)(m%3-1)*0.5f;
			vectors[i] = Instantiate (VectorObj, new Vector2 (0, 0), Quaternion.identity);
			vectors[i].transform.position = new Vector2 (xx, -yy);
			vectors[i].transform.Rotate(new Vector3(0f, 0f, dv[m]));
		}
	}

	public void applyBoard (){					//apply color and pos on board
		int h = FieldCreate.h, w = FieldCreate.w;
		//apply put circle
		for (int i = 0; i < 4; i++) {
			int y = FieldCreate.playerY[i], x = FieldCreate.playerX[i];
			int vec = FieldCreate.posMove[i];
			Destroy(putCircle[i]);
			if (vec == -1)continue;
			float yy = y+(vec/3-1);
			float xx = x+(vec%3-1);
			putCircle[i] = Instantiate (CircleObj, new Vector2 (0, 0), Quaternion.identity);
			putCircle[i].transform.position = new Vector2 (xx, -yy);
			if(i == 0 || i == 1)
				putCircle[i].GetComponent<SpriteRenderer> ().color = new Color (1f, 0f, 0.5f, 0.5f);
			if(i == 2 || i == 3)
				putCircle[i].GetComponent<SpriteRenderer> ().color = new Color (0.5f, 0f, 1f, 0.5f);
		}
		//apply color
		for (int i = 0; i < h; i++) {
			for (int j = 0; j < w; j++) {
				Color tmp = new Color(1, 1, 1, 1);
				if (FieldCreate.board [i, j] == 1) tmp = new Color (0.7f, 0.3f, 0.3f, 1);
				if (FieldCreate.board [i, j] == 2) tmp = new Color (0.3f, 0.3f, 0.7f, 1);
				FieldCreate.boxes [i, j].GetComponent<SpriteRenderer> ().color = tmp;
			}
		}
		//apply player pos color
		for (int i = 0; i < 4; i++) {
			Color tmp = new Color(1, 1, 1, 1);
			if (i == 0 || i == 1)tmp = new Color (1, 0, 0, 1);
			if (i == 2 || i == 3)tmp = new Color (0, 0, 1, 1);
			int y = FieldCreate.playerY [i], x = FieldCreate.playerX [i];
			FieldCreate.boxes [y, x].GetComponent<SpriteRenderer> ().color = tmp;
		}
	}

	public void destroy(int i){
		//Debug.Log ("destroyed vectors");
		Destroy(vectors[i]);
	}

	void Start () {
		
	}
	void Update () {
		
	}
}

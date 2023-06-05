using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ScoreScript : MonoBehaviour {
	public static string redStr = "";
	public static string blueStr = "";
	public static int[] scoreInt = new int[2];
	public GameObject scoreRed;
	public GameObject scoreBlue;
	public GameObject objTime;
	public static float timeFloat = 0;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		timeFloat += Time.deltaTime;
		redStr = "Score red : " + scoreInt[0].ToString();
		blueStr = "\nScore blue: " + scoreInt[1].ToString();
		scoreRed.GetComponent<Text> ().text = redStr;
		scoreBlue.GetComponent<Text> ().text = blueStr;
		string str = "turn: " + NextStepScript.turnCount.ToString () + " \n";
		str += "time: " + ((int)timeFloat).ToString();
		objTime.GetComponent<Text> ().text = str + " ";
	}
}

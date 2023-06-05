using UnityEngine;
using System.Collections;

public class SetPlayerRed : MonoBehaviour {

	private int selectedToggleNum = 0;
	private int sliderNum;
	private int drop;

	public void SetToggleNum(int toggleNum) {
		selectedToggleNum = toggleNum;
		Debug.Log(selectedToggleNum);
	}

	public void SetSliderValue(int sliderNum) {
		this.sliderNum = sliderNum;
		Debug.Log(this.sliderNum);
	}

	public void OnDrop(int dropNum) {
		drop = dropNum;
		Debug.Log("selected player: " + drop);

		GameObject field = GameObject.Find ("Field");
		Chat chat = field.GetComponent<Chat>();
		chat.SendCommand ("2 0 " + drop);

		strAnalyze analysis = field.GetComponent<strAnalyze>();
		for(int i = 0;i < 2;i++)analysis.destroy (i);
	}
}
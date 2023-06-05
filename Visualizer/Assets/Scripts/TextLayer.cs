using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using UnityEngine;
using System.Collections;

public class TextLayer : MonoBehaviour {

	public string LayerName;
	public int SortingOrder;
	GameObject selectText;
	GameObject[] infoText = new GameObject[2];

	void Start () {
		infoText [0] = GameObject.Find ("InfoText(Red)");
		infoText [1] = GameObject.Find ("InfoText(Blue)");
		selectText = GameObject.Find ("SelectPlayerText");
	}

	void Update () {
		for (int i = 0; i < 2; i++) {
			infoText[i].GetComponent <Renderer>().sortingLayerName = LayerName;
			infoText[i].GetComponent <Renderer>().sortingOrder = SortingOrder;
		}
		this.GetComponent <Renderer>().sortingLayerName = LayerName;
		this.GetComponent <Renderer>().sortingOrder = SortingOrder;
		selectText.GetComponent <Renderer>().sortingLayerName = LayerName;
		selectText.GetComponent <Renderer>().sortingOrder = SortingOrder;
	}
}
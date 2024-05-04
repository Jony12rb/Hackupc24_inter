from gradio_client import Client, file

client = Client("https://fe5b142938cf1e9296.gradio.live/")
result = client.predict(
		model="facebook/musicgen-medium",
        model_path = "",
		decoder="Default",
		text="Summer trip",
		melody=None,
		duration=10,
		topk=250,
		topp=0,
		temperature=1,
		cfg_coef=3,
		api_name="/predict_full"
)
print(result)
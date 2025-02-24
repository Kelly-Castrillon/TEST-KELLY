from PIL import Image
from landingai.predict import SnowflakeNativeAppPredictor
url = "http://b4c4qqkz-rpwerko-lai-snow-product-mgmt.snowflakecomputing.app"
# Load your image
image = Image.open("/Users/kellycastrillon/DATASETS/Tests-do_not_delete/DATASET- CON PASCAL OD/handsx-ray-170544090241/handsx-ray-170544090241/dev/Images/2023-04-20T17-40-17-549Z-image3_png_jpg.rf.4bb8448a11e543676717a28ef076ca1e.jpg")
# Run inference
predictor = SnowflakeNativeAppPredictor(
  endpoint_id="c7192fbc-9e1b-4849-8f62-5cfa6589a156"
  native_app_url=url,
  snowflake_account="IPB83164"
  snowflake_user="PRODUCT_SHARED_ACCOUNT"
  snowflake_password="NativeApp5"
  # or, in case of private key auth, use the following instead of `snowflake_password`:
  # snowflake_private_key="-----BEGIN PRIVATE KEY-----\nMIIEvg...",
)
predictions = predictor.predict(image)
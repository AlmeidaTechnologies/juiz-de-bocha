import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;

Uri __prepareUri(String endpoint, Map<String, dynamic> queryParameters) {
  Uri uri = Uri.parse('http://localhost:8080$endpoint');
  // Uri uri = Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app$endpoint');
  uri = uri.replace(queryParameters: queryParameters);
  return uri;
}

Future<http.ByteStream> __processImage(Uri uri, Uint8List bytes) async {
  http.Request request = http.Request('POST', uri);
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  return await response.stream;
}

Future<String> processImageReturnURL(
    File img,
    {
      String? userID,
      double? accelerometer,
      double? gyroscope,
      double? lensAperture,
      double? sensorSensitivity,
      int? sensorExposureTime,
    }
) async {
  return (await __processImage(
    __prepareUri('/url', {
      'userID': userID,
      'accelerometer': accelerometer.toString(),
      'gyroscope': gyroscope.toString(),
      'lensAperture': lensAperture.toString(),
      'sensorSensitivity': sensorSensitivity.toString(),
      'sensorExposureTime': sensorExposureTime.toString(),
    }),
    await img.readAsBytes()
  )).bytesToString();
}

Future<File> processImageReturnImage(
    File img, String pathResultado,
    {
      String? userID,
      double? accelerometer,
      double? gyroscope,
      double? lensAperture,
      double? sensorSensitivity,
      int? sensorExposureTime,
    }
) async {
  File res = File(pathResultado);
  Uint8List bytes = await (await __processImage(
    __prepareUri('/image', {
      'userID': userID,
      'accelerometer': accelerometer.toString(),
      'gyroscope': gyroscope.toString(),
      'lensAperture': lensAperture.toString(),
      'sensorSensitivity': sensorSensitivity.toString(),
      'sensorExposureTime': sensorExposureTime.toString(),
    }),
    await img.readAsBytes(),
  )).toBytes();
  await res.writeAsBytes(bytes);
  return res;
}

////////// Exemplos de uso //////////
void main(List<String> args){
  File img = File(args.isEmpty ? 'test.jpg' : args[0]);
  processImageReturnImage(
    img,
    "result.gif",
    userID: "1",
    accelerometer: 2.9,
  );
  // processImageReturnURL(
  //   img,
  //   userID: "1",
  //   accelerometer: 2.9,
  // );
}

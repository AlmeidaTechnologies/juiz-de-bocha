import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, Uint8List>> processImage(
    Uint8List bytes,
    {
      String? userID,
      double? accelerometer,
      double? gyroscope,
      double? lensAperture,
      double? sensorSensitivity,
      int? sensorExposureTime,
    }
) async {

  Uri uri = Uri.parse('http://localhost:8080/image');
  // Uri uri = Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app/image');
  uri = uri.replace(queryParameters: {
    'userID': userID,
    'accelerometer': accelerometer,
    'gyroscope': gyroscope,
    'lensAperture': lensAperture,
    'sensorSensitivity': sensorSensitivity,
    'sensorExposureTime': sensorExposureTime,
    'with-thumbnail': 'true',
  });
  http.Request request = http.Request('POST', uri);
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  String data = await response.stream.bytesToString();
  Map<String, dynamic> json = jsonDecode(data);
  Map<String, Uint8List> files = {};
  Codec<String, String> stringToBase64 = utf8.fuse(base64);
  for (String key in json.keys){
    String encoded = json[key]!;
    files[key] = base64.decode(encoded.replaceAll('\n',''));
  }
  return files;
}

Future<Map<String, File>> testSingle(String? input) async {
  File img = File(input ?? 'test.jpg');
  Map<String, Uint8List> files = await processImage(await img.readAsBytes());
  File gif = File('result.gif');
  await gif.writeAsBytes(files['gif']!);
  File thumbnail = File('thumbnail.jpg');
  await thumbnail.writeAsBytes(files['thumbnail']!);
  return {
    'gif': gif,
    'thumbnail': thumbnail,
  };
}

void testSeveral(List<String> args) async {
  File img = File(args[0]);
  var bytes = await img.readAsBytes();
  var tests = [];
  for (int i = 0; i < 1; i++) {
    print("starting $i");
    tests.add(processImage(bytes));
    await Future.delayed(Duration(milliseconds: 500));
  }
  for (var test in tests){
    print("awaiting");
    var response = await test;
    print("response: $response");
  }
}

void main(List<String> args){
  testSingle(args.first);
  //testSeveral(args);
}

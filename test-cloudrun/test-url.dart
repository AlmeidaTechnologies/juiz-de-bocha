import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:collection/collection.dart';

// Camera data: https://pub.dev/documentation/camera/latest/camera/CameraImage-class.html

Future<Map<String, dynamic>> processImage(
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
  Uri uri = Uri.parse('http://localhost:8080/url');
  // Uri uri = Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app/url');
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
  return jsonDecode(data);
}

void testSingle(
    String? filepath,
    {
      String? user_id,
      double? accelerometer,
      double? gyroscope,
      double? lensAperture,
      double? sensorSensitivity,
      int? sensorExposureTime,
    }
) async {
  File img = File(filepath ?? 'test.jpg');
  Map<String, dynamic> urls = await processImage(await img.readAsBytes());
  print(urls);
}

void testSeveral(List<String> args) async {
  print(args[0]);
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
  testSingle(args.firstOrNull);
  //testSeveral(args);
}

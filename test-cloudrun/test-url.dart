import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:collection/collection.dart';

Future<String> processImage(Uint8List bytes) async {
  http.Request request = http.Request(
    'POST',
    Uri.parse('http://localhost:8080/url'),
    // Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app/url')
  );
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  return await response.stream.bytesToString();
}

void testSingle(String? filepath) async {
  File img = File(filepath ?? 'test.jpg');
  String url = await processImage(await img.readAsBytes());
  print(url);
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

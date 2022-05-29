import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Uint8List> processImage(Uint8List bytes) async {
  http.Request request = http.Request(
    'POST',
    Uri.parse('http://localhost:8080/image'),
    // Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app/image')
  );
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  return await response.stream.toBytes();
}

Future<File> testSingle() async {
  File img = File('test.jpg');
  File res = File('result.gif');
  await res.writeAsBytes(await processImage(await img.readAsBytes()));
  return res;
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
  testSingle();
  //testSeveral(args);
}

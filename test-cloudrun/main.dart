import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<String> processImage(Uint8List bytes) async {
  var request = await http.Request(
    'POST',
    // Uri.parse('http://localhost:8080'),
    Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app')
  );
  // request.headers.clear();
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  var response = await request.send();
  return await response.stream.bytesToString();
}

void main() async {
  File img = File('test.jpg');
  var url = await processImage(await img.readAsBytes());
  print(url);
}

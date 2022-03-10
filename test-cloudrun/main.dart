import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

Future<Uint8List> processImage(Uint8List bytes) async {
  var request = await http.Request(
    'POST',
    Uri.parse('http://localhost:8080'),
    // Uri.parse('https://jsonplaceholder.typicode.com/albums/1')
  );
  // request.headers.clear();
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  var response = await request.send();
  return response.stream.toBytes();
}

void main() async {
  File img = File('test.jpg');
  var bytes = await processImage(await img.readAsBytes());
  File res = File('result.jpg');
  await res.writeAsBytes(bytes);
}

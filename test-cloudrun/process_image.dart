import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<http.ByteStream> _processImage(Uint8List bytes) async {
  http.Request request = http.Request(
    'POST',
    Uri.parse('https://recognizer-usnztkx52q-rj.a.run.app')
  );
  request.headers.addAll({
    'Keep-Alive': 'timeout=100, max=100',
  });
  request.bodyBytes = bytes;
  http.StreamedResponse response = await request.send();
  return response.stream;
}

Future<File> testSingle(File foto, String pathResultado) async {
  File res = File(pathResultado);
  IOSink writeStream = res.openWrite();
  await writeStream.addStream(await _processImage(await foto.readAsBytes()));
  await writeStream.close();
  return res;
}

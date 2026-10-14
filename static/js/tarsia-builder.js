/* Interactive Tarsia triangle-jigsaw builder: live SVG preview + export.
 * Geometry mirrors apps/resources/generators/tarsia_geom.py exactly, so the
 * live preview and the server-rendered PDF/PPTX match. See that module (and
 * tools/tarsia/geom.py, the original) for the derivation. */
(function () {
  'use strict';

  var SQRT3 = Math.sqrt(3);

  function rowUpApexX(r, i, s) {
    return (-r * s) / 2 + i * s - s / 2;
  }

  function triangleVertices(n, s) {
    var h = (s * SQRT3) / 2;
    var tris = {};
    for (var r = 1; r <= n; r++) {
      var top = (r - 1) * h;
      var bot = r * h;
      for (var i = 1; i <= r; i++) {
        var ax = rowUpApexX(r, i, s);
        tris[r + ',U,' + i] = [[ax, top], [ax - s / 2, bot], [ax + s / 2, bot]];
      }
      for (var j = 1; j < r; j++) {
        var axj = rowUpApexX(r, j, s);
        var axj1 = rowUpApexX(r, j + 1, s);
        tris[r + ',D,' + j] = [[axj, top], [axj1, top], [axj + s / 2, bot]];
      }
    }
    return tris;
  }

  function internalEdges(n, s) {
    var tris = triangleVertices(n, s);
    var edges = [];
    for (var r = 1; r <= n; r++) {
      for (var i = 1; i < r; i++) {
        var a = tris[r + ',U,' + i];
        var mx = (a[0][0] + a[2][0]) / 2;
        var my = (a[0][1] + a[2][1]) / 2;
        var angle = (Math.atan2(a[2][1] - a[0][1], a[2][0] - a[0][0]) * 180) / Math.PI;
        edges.push({ ka: r + ',U,' + i, kb: r + ',D,' + i, mid: [mx, my], angle: angle });
      }
      for (var i2 = 1; i2 < r; i2++) {
        var d = tris[r + ',D,' + i2];
        var mx2 = (d[1][0] + d[2][0]) / 2;
        var my2 = (d[1][1] + d[2][1]) / 2;
        var angle2 = (Math.atan2(d[2][1] - d[1][1], d[2][0] - d[1][0]) * 180) / Math.PI;
        edges.push({ ka: r + ',D,' + i2, kb: r + ',U,' + (i2 + 1), mid: [mx2, my2], angle: angle2 });
      }
    }
    for (var r2 = 1; r2 < n; r2++) {
      for (var i3 = 1; i3 <= r2; i3++) {
        var u = tris[r2 + ',U,' + i3];
        var key2 = (r2 + 1) + ',D,' + i3;
        if (tris[key2]) {
          var mx3 = (u[1][0] + u[2][0]) / 2;
          var my3 = (u[1][1] + u[2][1]) / 2;
          edges.push({ ka: r2 + ',U,' + i3, kb: key2, mid: [mx3, my3], angle: 0 });
        }
      }
    }
    return edges;
  }

  function centroid(verts) {
    var x = (verts[0][0] + verts[1][0] + verts[2][0]) / 3;
    var y = (verts[0][1] + verts[1][1] + verts[2][1]) / 3;
    return [x, y];
  }

  function edgeCount(n) {
    return internalEdges(n, 1).length;
  }

  function textRotation(mid, verts, edgeAngle) {
    var c = centroid(verts);
    var rot = edgeAngle;
    for (var k = 0; k < 2; k++) {
      var cand = edgeAngle + k * 180;
      var rad = ((cand + 90) * Math.PI) / 180;
      var upX = Math.cos(rad);
      var upY = Math.sin(rad);
      var dx = c[0] - mid[0];
      var dy = c[1] - mid[1];
      if (upX * dx + upY * dy > 0) {
        rot = cand;
        break;
      }
    }
    return (((rot + 90) % 180) + 180) % 180 - 90;
  }

  var INK = '#1F2A44';

  function renderSVG(n, pairs, opts) {
    opts = opts || {};
    var s = opts.s || 1.8;
    var fontSize = opts.fontSize || 9;
    var insetFrac = opts.insetFrac || 0.11;
    var strokeWidth = opts.strokeWidth || 2;
    var margin = opts.margin || 0.2;

    var tris = triangleVertices(n, s);
    var edges = internalEdges(n, s);
    var width = n * s + 2 * margin;
    var height = (n * s * SQRT3) / 2 + 2 * margin;
    var scale = 100; // data units -> px-ish viewBox units

    var parts = [];
    parts.push(
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' +
        (width * scale).toFixed(1) +
        ' ' +
        (height * scale).toFixed(1) +
        '" font-family="Inter, system-ui, sans-serif">'
    );

    function tx(x) {
      return (x + width / 2) * scale;
    }
    function ty(y) {
      return (y + margin) * scale;
    }

    Object.keys(tris).forEach(function (key) {
      var v = tris[key];
      var d =
        'M ' + tx(v[0][0]) + ' ' + ty(v[0][1]) + ' L ' + tx(v[1][0]) + ' ' + ty(v[1][1]) + ' L ' + tx(v[2][0]) + ' ' + ty(v[2][1]) + ' Z';
      parts.push('<path d="' + d + '" fill="none" stroke="' + INK + '" stroke-width="' + strokeWidth + '" stroke-linejoin="round"/>');
    });

    var inset = insetFrac * s;
    edges.forEach(function (e, idx) {
      var pair = pairs[idx] || ['', ''];
      [
        [e.ka, pair[0]],
        [e.kb, pair[1]],
      ].forEach(function (pairItem) {
        var key = pairItem[0];
        var text = pairItem[1] || '';
        var verts = tris[key];
        if (!verts || !text) return;
        var rot = textRotation(e.mid, verts, e.angle);
        var c = centroid(verts);
        var dx = c[0] - e.mid[0];
        var dy = c[1] - e.mid[1];
        var dist = Math.hypot(dx, dy) || 1;
        var ux = dx / dist;
        var uy = dy / dist;
        var px = tx(e.mid[0] + ux * inset);
        var py = ty(e.mid[1] + uy * inset);
        var safe = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        parts.push(
          '<text x="' +
            px.toFixed(1) +
            '" y="' +
            py.toFixed(1) +
            '" transform="rotate(' +
            rot.toFixed(1) +
            ' ' +
            px.toFixed(1) +
            ' ' +
            py.toFixed(1) +
            ')" text-anchor="middle" dominant-baseline="middle" font-size="' +
            (fontSize * scale * 0.012).toFixed(1) +
            '" fill="' +
            INK +
            '">' +
            safe +
            '</text>'
        );
      });
    });

    parts.push('</svg>');
    return parts.join('');
  }

  window.TarsiaBuilder = {
    edgeCount: edgeCount,
    renderSVG: renderSVG,
  };
})();

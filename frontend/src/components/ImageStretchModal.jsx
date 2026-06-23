import React, { useState, useRef, useEffect, useCallback } from 'react';
import { X, Check, Maximize } from 'lucide-react';

const OUT_W = 1280;
const OUT_H = 720; // 16:9 output

const HANDLES = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];

const createImage = (url) =>
  new Promise((resolve, reject) => {
    const image = new Image();
    image.addEventListener('load', () => resolve(image));
    image.addEventListener('error', reject);
    image.setAttribute('crossOrigin', 'anonymous');
    image.src = url;
  });

export const ImageStretchModal = ({ imageSrc, onCancel, onCropDone }) => {
  const frameRef = useRef(null);
  const imgElRef = useRef(null);
  const [frame, setFrame] = useState({ w: 0, h: 0 });
  const [rect, setRect] = useState(null); // {x,y,w,h} in display px
  const [processing, setProcessing] = useState(false);
  const drag = useRef(null);

  // Measure frame and init image rect (contain) once frame is known
  useEffect(() => {
    const measure = () => {
      if (frameRef.current) {
        const r = frameRef.current.getBoundingClientRect();
        setFrame({ w: r.width, h: r.height });
      }
    };
    measure();
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, []);

  useEffect(() => {
    if (frame.w && imgElRef.current && !rect) {
      const img = imgElRef.current;
      const aspect = img.naturalWidth / img.naturalHeight;
      let w = frame.w;
      let h = w / aspect;
      if (h > frame.h) {
        h = frame.h;
        w = h * aspect;
      }
      setRect({ x: (frame.w - w) / 2, y: (frame.h - h) / 2, w, h });
    }
  }, [frame, rect]);

  const onImgLoad = () => {
    if (frame.w && !rect) setFrame((f) => ({ ...f })); // trigger init effect
  };

  const startDrag = (e, type) => {
    e.preventDefault();
    e.stopPropagation();
    drag.current = {
      type,
      startX: e.clientX,
      startY: e.clientY,
      orig: { ...rect },
    };
  };

  const onMove = useCallback((e) => {
    if (!drag.current || !drag.current.orig) return;
    const { type, startX, startY, orig } = drag.current;
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    let { x, y, w, h } = orig;
    const MIN = 20;

    if (type === 'move') {
      x = orig.x + dx;
      y = orig.y + dy;
    } else {
      if (type.includes('e')) w = orig.w + dx;
      if (type.includes('s')) h = orig.h + dy;
      if (type.includes('w')) { x = orig.x + dx; w = orig.w - dx; }
      if (type.includes('n')) { y = orig.y + dy; h = orig.h - dy; }
      if (w < MIN) w = MIN;
      if (h < MIN) h = MIN;
    }
    setRect({ x, y, w, h });
  }, []);

  const endDrag = useCallback(() => {
    drag.current = null;
  }, []);

  useEffect(() => {
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', endDrag);
    return () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', endDrag);
    };
  }, [onMove, endDrag]);

  const fitToFrame = () => {
    setRect({ x: 0, y: 0, w: frame.w, h: frame.h });
  };

  const handleConfirm = async () => {
    if (!rect || !frame.w) return;
    setProcessing(true);
    try {
      const img = await createImage(imageSrc);
      const scale = OUT_W / frame.w;
      const canvas = document.createElement('canvas');
      canvas.width = OUT_W;
      canvas.height = OUT_H;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, OUT_W, OUT_H);
      ctx.drawImage(
        img,
        rect.x * scale,
        rect.y * scale,
        rect.w * scale,
        rect.h * scale
      );
      const blob = await new Promise((res) => canvas.toBlob(res, 'image/jpeg', 0.92));
      await onCropDone(blob);
    } finally {
      setProcessing(false);
    }
  };

  const handleStyle = (pos) => {
    const map = {
      nw: { left: -6, top: -6, cursor: 'nwse-resize' },
      n: { left: '50%', top: -6, marginLeft: -6, cursor: 'ns-resize' },
      ne: { right: -6, top: -6, cursor: 'nesw-resize' },
      e: { right: -6, top: '50%', marginTop: -6, cursor: 'ew-resize' },
      se: { right: -6, bottom: -6, cursor: 'nwse-resize' },
      s: { left: '50%', bottom: -6, marginLeft: -6, cursor: 'ns-resize' },
      sw: { left: -6, bottom: -6, cursor: 'nesw-resize' },
      w: { left: -6, top: '50%', marginTop: -6, cursor: 'ew-resize' },
    };
    return map[pos];
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4 z-[60]"
      data-testid="image-stretch-modal"
    >
      <div className="bg-white rounded-2xl max-w-2xl w-full overflow-hidden">
        <div className="p-5 border-b border-gray-200 flex justify-between items-center">
          <div>
            <h3 className="text-lg font-bold text-gray-900">Resize & Fit Image</h3>
            <p className="text-sm text-gray-500">Drag the handles to stretch the image; drag the image to move it (card is 16:9)</p>
          </div>
          <button
            onClick={onCancel}
            data-testid="stretch-cancel-x"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            disabled={processing}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-5">
          <div
            ref={frameRef}
            className="relative w-full bg-gray-100 border-2 border-dashed border-gray-300 overflow-hidden select-none"
            style={{ aspectRatio: '16 / 9', touchAction: 'none' }}
            data-testid="stretch-frame"
          >
            {/* image being positioned/stretched */}
            <img
              ref={imgElRef}
              src={imageSrc}
              alt="preview"
              onLoad={onImgLoad}
              draggable={false}
              onPointerDown={(e) => startDrag(e, 'move')}
              style={
                rect
                  ? {
                      position: 'absolute',
                      left: rect.x,
                      top: rect.y,
                      width: rect.w,
                      height: rect.h,
                      cursor: 'move',
                    }
                  : { opacity: 0 }
              }
            />
            {rect && (
              <div
                className="absolute border-2 border-blue-500"
                style={{ left: rect.x, top: rect.y, width: rect.w, height: rect.h, pointerEvents: 'none' }}
              >
                {HANDLES.map((pos) => (
                  <div
                    key={pos}
                    data-testid={`stretch-handle-${pos}`}
                    onPointerDown={(e) => startDrag(e, pos)}
                    className="absolute w-3 h-3 bg-white border-2 border-blue-500 rounded-sm"
                    style={{ ...handleStyle(pos), pointerEvents: 'auto' }}
                  />
                ))}
              </div>
            )}
          </div>

          <button
            type="button"
            onClick={fitToFrame}
            data-testid="stretch-fit-btn"
            className="mt-3 inline-flex items-center space-x-2 px-4 py-2 text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors text-sm"
          >
            <Maximize className="w-4 h-4" />
            <span>Stretch to fill card</span>
          </button>
        </div>

        <div className="px-5 py-4 flex justify-end space-x-3 border-t border-gray-100">
          <button
            type="button"
            onClick={onCancel}
            data-testid="stretch-cancel-btn"
            className="px-5 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            disabled={processing}
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            data-testid="stretch-confirm-btn"
            className="flex items-center space-x-2 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            disabled={processing || !rect}
          >
            {processing ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <Check className="w-4 h-4" />
                <span>Apply & Upload</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageStretchModal;

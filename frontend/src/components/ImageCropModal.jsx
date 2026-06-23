import React, { useState, useCallback } from 'react';
import Cropper from 'react-easy-crop';
import { X, ZoomIn, Check } from 'lucide-react';

const createImage = (url) =>
  new Promise((resolve, reject) => {
    const image = new Image();
    image.addEventListener('load', () => resolve(image));
    image.addEventListener('error', (error) => reject(error));
    image.setAttribute('crossOrigin', 'anonymous');
    image.src = url;
  });

const getCroppedBlob = async (imageSrc, cropPixels) => {
  const image = await createImage(imageSrc);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = cropPixels.width;
  canvas.height = cropPixels.height;
  ctx.drawImage(
    image,
    cropPixels.x,
    cropPixels.y,
    cropPixels.width,
    cropPixels.height,
    0,
    0,
    cropPixels.width,
    cropPixels.height
  );
  return new Promise((resolve) => {
    canvas.toBlob((blob) => resolve(blob), 'image/jpeg', 0.92);
  });
};

export const ImageCropModal = ({ imageSrc, aspect = 16 / 9, onCancel, onCropDone }) => {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  const [processing, setProcessing] = useState(false);

  const onCropComplete = useCallback((_, areaPixels) => {
    setCroppedAreaPixels(areaPixels);
  }, []);

  const handleConfirm = async () => {
    if (!croppedAreaPixels) return;
    setProcessing(true);
    try {
      const blob = await getCroppedBlob(imageSrc, croppedAreaPixels);
      await onCropDone(blob);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4 z-[60]"
      data-testid="image-crop-modal"
    >
      <div className="bg-white rounded-2xl max-w-2xl w-full overflow-hidden">
        <div className="p-5 border-b border-gray-200 flex justify-between items-center">
          <div>
            <h3 className="text-lg font-bold text-gray-900">Crop & Preview Image</h3>
            <p className="text-sm text-gray-500">Drag to reposition, zoom to adjust the best fit (16:9)</p>
          </div>
          <button
            onClick={onCancel}
            data-testid="crop-cancel-x"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            disabled={processing}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="relative w-full h-80 bg-gray-900">
          <Cropper
            image={imageSrc}
            crop={crop}
            zoom={zoom}
            aspect={aspect}
            onCropChange={setCrop}
            onZoomChange={setZoom}
            onCropComplete={onCropComplete}
          />
        </div>

        <div className="px-5 py-4 flex items-center space-x-3 border-t border-gray-100">
          <ZoomIn className="w-5 h-5 text-gray-500" />
          <input
            type="range"
            min={1}
            max={3}
            step={0.01}
            value={zoom}
            onChange={(e) => setZoom(Number(e.target.value))}
            data-testid="crop-zoom-slider"
            className="flex-1 accent-blue-600"
          />
        </div>

        <div className="px-5 py-4 flex justify-end space-x-3 border-t border-gray-100">
          <button
            type="button"
            onClick={onCancel}
            data-testid="crop-cancel-btn"
            className="px-5 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            disabled={processing}
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            data-testid="crop-confirm-btn"
            className="flex items-center space-x-2 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            disabled={processing}
          >
            {processing ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <Check className="w-4 h-4" />
                <span>Crop & Upload</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageCropModal;

import React, { useState } from 'react';

export default function App() {
  const [keys, setKeys] = useState({ public_key: '', private_key: '' });
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [mode, setMode] = useState('encrypt');
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:8080';

  const generateKeys = async () => {
    try {
      const res = await fetch(`${API_URL}/generate-keys`, { method: 'POST' });
      const data = await res.json();
      setKeys({ public_key: data.public_key, private_key: data.private_key });
    } catch (e) {
      setError("System failure: Unable to securely generate cryptographic keys.");
    }
  };

  const handleModeSwitch = (newMode) => {
    setMode(newMode);
    setText('');
    setResult(null);
    setError(null);
  };

  const handleProcess = async () => {
    setError(null);
    setResult(null);

    const endpoint = mode === 'encrypt' ? '/encrypt' : '/decrypt';
    
    let decryptPayload = null;
    if (mode === 'decrypt') {
      try {
        decryptPayload = JSON.parse(atob(text));
        if (!decryptPayload.c || !decryptPayload.k || !decryptPayload.n) {
          throw new Error();
        }
      } catch (e) {
        setError("Data error: Invalid payload block. Expected Base64 JSON sequence.");
        return;
      }
    }

    const payload = mode === 'encrypt' 
      ? { text, public_key: keys.public_key }
      : { 
          private_key: keys.private_key,
          ciphertext_base64: decryptPayload.c,
          wrapped_key_base64: decryptPayload.k,
          nonce_base64: decryptPayload.n
        };

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) {
        const errMsg = typeof data.detail === 'object' ? JSON.stringify(data.detail) : data.detail;
        throw new Error(errMsg || "Operation halted.");
      }
      
      setResult(data);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="min-h-screen text-arch-text flex items-center justify-center p-8 bg-transparent">
      
      {/* Main Architectural Card */}
      <div className="w-full max-w-[1400px] h-[85vh] bg-arch-surface shadow-2xl flex flex-col lg:flex-row overflow-hidden relative">
        
        {/* LEFT COLUMN: Narrative & Controls (Light Mode) */}
        <div className="w-full lg:w-5/12 h-full flex flex-col p-12 overflow-y-auto">
          
          <div className="flex-1 space-y-12 pr-4">
            {/* Title Block */}
            <div className="space-y-4 pt-12">
              <h1 className="text-4xl lg:text-5xl font-light tracking-tight text-black">
                CIPHER<br />
                <span className="font-bold">LINGO</span>
              </h1>
              <p className="text-xs text-arch-muted max-w-[280px] leading-relaxed tracking-wider">
                A deterministic, mathematically seeded universal polyglot transformer. Encrypt unstructured data via an entropy-resistant linguistic cipher.
              </p>
            </div>

            {/* Error Banner */}
            {error && (
              <div className="border border-red-200 bg-red-50 text-red-800 p-4 text-xs tracking-wider">
                <strong>[EXCEPTION]</strong> {error}
              </div>
            )}

            {/* Mode Switcher */}
            <div className="flex items-center gap-8 border-b border-arch-border pb-4">
              <button 
                className={`text-xs uppercase tracking-widest transition-colors ${mode === 'encrypt' ? 'text-black font-bold' : 'text-arch-muted hover:text-black'}`}
                onClick={() => handleModeSwitch('encrypt')}
              >
                01. Encrypt
              </button>
              <button 
                className={`text-xs uppercase tracking-widest transition-colors ${mode === 'decrypt' ? 'text-black font-bold' : 'text-arch-muted hover:text-black'}`}
                onClick={() => handleModeSwitch('decrypt')}
              >
                02. Decrypt
              </button>
            </div>

            {/* Form Inputs */}
            <div className="space-y-8">
              
              {/* RSA Configuration */}
              <div className="space-y-2">
                <div className="flex items-end justify-between mb-2">
                  <label className="text-[10px] uppercase tracking-widest text-black font-bold">
                    {mode === 'encrypt' ? 'A. Public Key Array' : 'A. Private Key Array'}
                  </label>
                  <button 
                    onClick={generateKeys}
                    className="text-[10px] uppercase tracking-widest text-arch-muted hover:text-black transition-colors"
                  >
                    Generate Pairs
                  </button>
                </div>
                
                {mode === 'encrypt' ? (
                  <textarea 
                    className="arch-input h-16"
                    value={keys.public_key}
                    onChange={(e) => setKeys({...keys, public_key: e.target.value})}
                    placeholder="Provide RSA 2048-bit Public Key..."
                  />
                ) : (
                  <textarea 
                    className="arch-input h-16 bg-[#fafafa]"
                    value={keys.private_key}
                    onChange={(e) => setKeys({...keys, private_key: e.target.value})}
                    placeholder="Provide RSA 2048-bit Private Key..."
                  />
                )}
              </div>

              {/* Main Payload */}
              <div className="space-y-2">
                <label className="text-[10px] uppercase tracking-widest text-black font-bold block mb-2">
                  {mode === 'encrypt' ? 'B. Plaintext Matrix' : 'B. Encrypted Payload Sequence'}
                </label>
                <textarea 
                  className="arch-input h-32"
                  placeholder={mode === 'encrypt' ? "Input source material..." : "Input ciphertext sequence..."}
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
              </div>

            </div>
          </div>

          {/* Action Trigger */}
          <div className="pt-8 border-t border-arch-border mt-8">
            <button 
              onClick={handleProcess}
              className="w-full bg-black text-white text-xs uppercase tracking-widest py-5 hover:bg-[#222] active:bg-[#000] transition-colors font-medium flex items-center justify-between px-6"
            >
              <span>{mode === 'encrypt' ? 'Execute Encryption' : 'Execute Decryption'}</span>
              <span>→</span>
            </button>
          </div>

        </div>

        {/* RIGHT COLUMN: Dark Mode Diagram (60%) */}
        <div className="w-full lg:w-7/12 h-full bg-arch-dark text-[#e0e0e0] flex flex-col p-12 overflow-y-auto relative">
          
          <div className="border-b border-[#333] pb-6 mb-12 flex justify-between items-end">
            <h2 className="text-xl font-light tracking-tight">Active Pipeline Node</h2>
            <span className="text-[10px] uppercase tracking-widest text-[#666]">System Telemetry</span>
          </div>

          <div className="flex-1 flex flex-col">
            {!result ? (
              <div className="m-auto flex flex-col items-center justify-center opacity-30">
                {/* Thin line art constellation representation */}
                <div className="w-px h-32 bg-white mb-8"></div>
                <div className="w-2 h-2 bg-transparent border border-white rounded-full"></div>
                <div className="text-[10px] uppercase tracking-widest mt-8">Awaiting Input Stream</div>
              </div>
            ) : (
              <div className="space-y-12 animate-fade-in relative container-lines pl-4">
                
                {/* Visual connecting line behind steps */}
                <div className="absolute top-0 bottom-0 left-[21px] w-[0.5px] bg-[#333] z-0"></div>

                {result.pipeline && Object.entries(result.pipeline).map(([stepName, stepVal], idx) => (
                  <div key={idx} className="relative z-10 flex gap-8">
                    
                    {/* Minimal Node */}
                    <div className="flex flex-col items-center pt-1">
                      <div className="w-[9px] h-[9px] bg-arch-dark border border-white rounded-full"></div>
                    </div>
                    
                    {/* Node Data */}
                    <div className="flex-1">
                      <h3 className="text-[10px] uppercase tracking-widest text-[#888] mb-4">
                        Step {idx + 1} — {stepName.replace(/_/g, " ")}
                      </h3>
                      <div className="text-sm font-light tracking-wider leading-relaxed break-all text-white">
                         {typeof stepVal === 'boolean' ? (stepVal ? 'Verified' : 'Invalidated') : stepVal}
                      </div>
                    </div>

                  </div>
                ))}

              </div>
            )}
          </div>

          {/* FINAL DATA BLOCK */}
          {result && (
            <div className="mt-12 border-t border-[#333] pt-8">
               <h3 className="text-[10px] uppercase tracking-widest text-[#888] mb-4">Final Sequence Output</h3>
               <div className="bg-[#111] border border-[#222] p-6 text-xs text-[#00ffcc] font-mono tracking-widest break-all shadow-[0_4px_30px_rgba(0,0,0,0.5)]">
                 {mode === 'encrypt' 
                   ? btoa(JSON.stringify({ c: result.ciphertext_base64, k: result.wrapped_key_base64, n: result.nonce_base64 }))
                   : result.plaintext
                 }
               </div>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}

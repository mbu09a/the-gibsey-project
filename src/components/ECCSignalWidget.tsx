import React, { useState, useEffect } from 'react';

export type ECCStatus = 'clean' | 'corrected' | 'error';

interface ECCSignalWidgetProps {
  status?: ECCStatus;
  errorCount?: number;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

const ECCSignalWidget: React.FC<ECCSignalWidgetProps> = ({
  status = 'clean',
  errorCount = 0,
  className = '',
  size = 'md'
}) => {
  const [isAnimating, setIsAnimating] = useState(false);

  // Trigger animation when status changes
  useEffect(() => {
    if (status === 'corrected') {
      setIsAnimating(true);
      const timer = setTimeout(() => setIsAnimating(false), 1000);
      return () => clearTimeout(timer);
    }
  }, [status, errorCount]);

  const getStatusConfig = () => {
    switch (status) {
      case 'clean':
        return {
          color: '#00FF41',
          bgColor: '#00FF4120',
          icon: '●',
          label: 'CLEAN',
          description: 'Signal clear'
        };
      case 'corrected':
        return {
          color: '#FFD700',
          bgColor: '#FFD70020',
          icon: '◐',
          label: `RS-${errorCount}`,
          description: `Reed-Solomon corrected ${errorCount} error${errorCount !== 1 ? 's' : ''}`
        };
      case 'error':
        return {
          color: '#FF4444',
          bgColor: '#FF444420',
          icon: '◯',
          label: 'ERROR',
          description: 'Uncorrectable transmission'
        };
    }
  };

  const getSizeConfig = () => {
    switch (size) {
      case 'sm':
        return {
          container: 'px-2 py-1 text-xs',
          icon: 'text-sm',
          spacing: 'gap-1'
        };
      case 'md':
        return {
          container: 'px-3 py-2 text-sm',
          icon: 'text-base',
          spacing: 'gap-2'
        };
      case 'lg':
        return {
          container: 'px-4 py-3 text-base',
          icon: 'text-lg',
          spacing: 'gap-3'
        };
    }
  };

  const statusConfig = getStatusConfig();
  const sizeConfig = getSizeConfig();

  return (
    <div 
      className={`
        inline-flex items-center font-mono rounded border
        transition-all duration-300
        ${sizeConfig.container} ${sizeConfig.spacing}
        ${isAnimating ? 'animate-pulse' : ''}
        ${className}
      `}
      style={{
        color: statusConfig.color,
        backgroundColor: statusConfig.bgColor,
        borderColor: statusConfig.color,
        boxShadow: `0 0 8px ${statusConfig.color}40`
      }}
      title={statusConfig.description}
    >
      <span 
        className={`${sizeConfig.icon} transition-all duration-200`}
        style={{
          filter: isAnimating ? `drop-shadow(0 0 4px ${statusConfig.color})` : undefined
        }}
      >
        {statusConfig.icon}
      </span>
      <span className="font-semibold">
        {statusConfig.label}
      </span>
    </div>
  );
};

export default ECCSignalWidget;
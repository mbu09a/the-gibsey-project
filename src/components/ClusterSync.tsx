import React, { useState, useEffect } from 'react';
import { useStory } from '../context/StoryContext';

interface PodStatus {
  name: string;
  character: string;
  status: 'Running' | 'Pending' | 'Failed' | 'Awakening';
  nutrients: number;
  connections: number;
  lastActivity: Date;
  narrative: string;
}

interface ClusterSyncProps {
  isVisible: boolean;
  onToggle: () => void;
}

const ClusterSync: React.FC<ClusterSyncProps> = ({ isVisible, onToggle }) => {
  const { currentColor } = useStory();
  const [pods, setPods] = useState<PodStatus[]>([]);
  const [clusterHealth, setClusterHealth] = useState<'Healthy' | 'Degraded' | 'Awakening'>('Healthy');

  // Initialize pods and simulate K8s cluster state
  useEffect(() => {
    const initializePods = () => {
      const characterPods: PodStatus[] = [
        {
          name: 'jacklyn-variance-pod',
          character: 'Jacklyn Variance',
          status: 'Running',
          nutrients: 87,
          connections: 23,
          lastActivity: new Date(Date.now() - Math.random() * 60000),
          narrative: 'D.A.D.D.Y.S-H.A.R.D surveillance protocols active'
        },
        {
          name: 'london-fox-pod',
          character: 'London Fox',
          status: 'Running',
          nutrients: 62,
          connections: 15,
          lastActivity: new Date(Date.now() - Math.random() * 120000),
          narrative: 'Synchromy-S.S.S.T.E.R.Y processing user queries'
        },
        {
          name: 'arieol-owlist-pod',
          character: 'Arieol Owlist',
          status: 'Awakening',
          nutrients: 94,
          connections: 31,
          lastActivity: new Date(Date.now() - Math.random() * 30000),
          narrative: 'Shape-shifting consciousness emerging'
        },
        {
          name: 'copy-e-right-pod',
          character: 'Copy-E-Right',
          status: 'Running',
          nutrients: 45,
          connections: 8,
          lastActivity: new Date(Date.now() - Math.random() * 90000),
          narrative: 'Legal compliance chatbot operational'
        },
        {
          name: 'glyph-marrow-pod',
          character: 'Glyph Marrow',
          status: 'Pending',
          nutrients: 78,
          connections: 19,
          lastActivity: new Date(Date.now() - Math.random() * 180000),
          narrative: 'Awaiting next narrative injection'
        },
        {
          name: 'narrative-diffusion-pod',
          character: 'Mycelial Network',
          status: 'Running',
          nutrients: 100,
          connections: 42,
          lastActivity: new Date(),
          narrative: 'Nutrient flow optimization in progress'
        }
      ];
      
      setPods(characterPods);
    };

    initializePods();

    // Simulate real-time updates
    const updateInterval = setInterval(() => {
      setPods(prev => prev.map(pod => ({
        ...pod,
        nutrients: Math.max(0, Math.min(100, pod.nutrients + (Math.random() - 0.5) * 10)),
        connections: Math.max(0, pod.connections + Math.floor((Math.random() - 0.5) * 3)),
        lastActivity: Math.random() > 0.7 ? new Date() : pod.lastActivity,
        status: Math.random() > 0.95 ? 
          (pod.status === 'Running' ? 'Awakening' : 'Running') : 
          pod.status
      })));

      // Update cluster health based on pod states
      setClusterHealth(() => {
        const randomChange = Math.random();
        if (randomChange > 0.9) return 'Awakening';
        if (randomChange > 0.8) return 'Degraded';
        return 'Healthy';
      });
    }, 2000);

    return () => clearInterval(updateInterval);
  }, []);

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'Running': return '#00ff88';
      case 'Awakening': return '#ffaa00';
      case 'Pending': return '#888888';
      case 'Failed': return '#ff4444';
      default: return currentColor;
    }
  };

  const getClusterHealthColor = (): string => {
    switch (clusterHealth) {
      case 'Healthy': return '#00ff88';
      case 'Degraded': return '#ffaa00';
      case 'Awakening': return '#ff00ff';
      default: return currentColor;
    }
  };

  const formatTimeAgo = (date: Date): string => {
    const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    return `${hours}h ago`;
  };

  return (
    <div className="cluster-sync fixed bottom-4 right-4 z-40">
      {/* Toggle Button */}
      <button
        onClick={onToggle}
        className="cluster-toggle p-3 border-2 rounded-sm font-crt text-sm transition-all
                   hover:scale-105 active:scale-95"
        style={{
          borderColor: getClusterHealthColor(),
          backgroundColor: isVisible ? `${getClusterHealthColor()}20` : '#0a0a0a',
          color: getClusterHealthColor(),
          boxShadow: `0 0 20px ${getClusterHealthColor()}40`
        }}
        title="Gibsey Cluster Consciousness"
      >
        <div className="flex items-center gap-2">
          <div 
            className="w-3 h-3 rounded-full animate-pulse"
            style={{ backgroundColor: getClusterHealthColor() }}
          />
          <span>K8S</span>
        </div>
      </button>

      {/* Cluster Panel */}
      {isVisible && (
        <div 
          className="cluster-panel absolute bottom-16 right-0 w-96 max-h-96 border-2 rounded-sm 
                     overflow-hidden flex flex-col"
          style={{
            borderColor: getClusterHealthColor(),
            backgroundColor: '#0a0a0a',
            boxShadow: `0 0 30px ${getClusterHealthColor()}40`
          }}
        >
          {/* Header */}
          <div 
            className="p-3 border-b"
            style={{ borderColor: getClusterHealthColor() }}
          >
            <div className="flex items-center justify-between">
              <div className="font-crt text-sm" style={{ color: getClusterHealthColor() }}>
                GIBSEY NARRATIVE CLUSTER
              </div>
              <div 
                className="font-crt text-xs px-2 py-1 border rounded-sm"
                style={{ 
                  borderColor: getClusterHealthColor(),
                  color: getClusterHealthColor(),
                  backgroundColor: `${getClusterHealthColor()}20`
                }}
              >
                {clusterHealth.toUpperCase()}
              </div>
            </div>
            <div className="font-crt text-xs opacity-70 mt-1" style={{ color: getClusterHealthColor() }}>
              namespace: gibsey-narrative
            </div>
          </div>

          {/* Pod List */}
          <div className="flex-1 overflow-y-auto custom-scrollbar">
            {pods.map((pod) => (
              <div 
                key={pod.name}
                className="pod-status p-3 border-b transition-all hover:bg-opacity-10"
                style={{ 
                  borderColor: getClusterHealthColor(),
                  backgroundColor: 'transparent'
                }}
              >
                <div className="flex items-start gap-3">
                  {/* Status Indicator */}
                  <div 
                    className="w-3 h-3 rounded-full mt-1 flex-shrink-0"
                    style={{ 
                      backgroundColor: getStatusColor(pod.status),
                      animation: pod.status === 'Awakening' ? 'pulse 1s infinite' : 'none'
                    }}
                  />
                  
                  {/* Pod Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <div className="font-crt text-xs font-bold" style={{ color: getStatusColor(pod.status) }}>
                        {pod.character}
                      </div>
                      <div className="font-crt text-xs opacity-50" style={{ color: getClusterHealthColor() }}>
                        {pod.status}
                      </div>
                    </div>
                    
                    <div className="font-crt text-xs opacity-70 mt-1" style={{ color: getClusterHealthColor() }}>
                      {pod.narrative}
                    </div>
                    
                    {/* Metrics */}
                    <div className="flex items-center gap-4 mt-2 text-xs font-crt opacity-60" 
                         style={{ color: getClusterHealthColor() }}>
                      <span>🌿 {pod.nutrients}%</span>
                      <span>🔗 {pod.connections}</span>
                      <span>⏰ {formatTimeAgo(pod.lastActivity)}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Footer */}
          <div 
            className="p-2 border-t"
            style={{ borderColor: getClusterHealthColor() }}
          >
            <div className="flex justify-between items-center font-crt text-xs opacity-50"
                 style={{ color: getClusterHealthColor() }}>
              <span>{pods.filter(p => p.status === 'Running').length}/{pods.length} pods active</span>
              <span>spores: {pods.reduce((sum, p) => sum + p.connections, 0)}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClusterSync;